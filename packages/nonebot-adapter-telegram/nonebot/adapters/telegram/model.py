from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Update(BaseModel):
    update_id: int
    message: Optional["Message_"]
    edited_message: Optional["Message_"]
    channel_post: Optional["Message_"]
    edited_channel_post: Optional["Message_"]
    inline_query: Optional["InlineQuery"]
    chosen_inline_result: Optional["ChosenInlineResult"]
    callback_query: Optional["CallbackQuery"]
    shipping_query: Optional["ShippingQuery"]
    pre_checkout_query: Optional["PreCheckoutQuery"]
    poll: Optional["Poll"]
    poll_answer: Optional["PollAnswer"]
    my_chat_member: Optional["ChatMemberUpdated"]
    chat_member: Optional["ChatMemberUpdated"]


class WebhookInfo(BaseModel):
    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: Optional[str]
    last_error_date: Optional[int]
    last_error_message: Optional[str]
    max_connections: Optional[int]
    allowed_updates: Optional[List[str]]


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    """
    :说明: 用户的语言编码，比如中文用户是 zh-hans

    :类型: ``Optional[str]``
    """
    can_join_groups: Optional[bool]
    """
    :说明: 是否可加入群聊，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """
    can_read_all_group_messages: Optional[bool]
    """
    :说明: 是否可以读取所有群消息，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """
    supports_inline_queries: Optional[bool]
    """
    :说明: 是否支持 inline_queries，只会在机器人的 get_me 方法中返回

    :类型: ``Optional[bool]``
    """


class Chat(BaseModel):
    id: int
    type: Literal["private", "group", "supergroup", "channel"]
    title: Optional[str]
    """
    :说明: 聊天标题，只会在聊天类型为 group supergroups channel 时返回

    :类型: ``Optional[str]``
    """
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    photo: Optional["ChatPhoto"]
    """
    :说明: 聊天图片，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPhoto]``
    """
    bio: Optional[str]
    """
    :说明: 聊天 ?，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    description: Optional[str]
    """
    :说明: 聊天简介，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    invite_link: Optional[str]
    """
    :说明: 邀请链接，仅在使用 get_chat 方法时返回

    :类型: ``Optional[str]``
    """
    pinned_message: Optional["Message_"]
    """
    :说明: 置顶消息，仅在使用 get_chat 方法时返回

    :类型: ``Optional[Message_]``
    """
    permissions: Optional["ChatPermissions"]
    """
    :说明: 成员权限，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatPermissions]``
    """
    slow_mode_delay: Optional[int]
    """
    :说明: 消息频率限制，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    message_auto_delete_time: Optional[int]
    """
    :说明: 消息自动撤回时间，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    sticker_set_name: Optional[str]
    """
    :说明: 聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[string]``
    """
    can_set_sticker_set: Optional[bool]
    """
    :说明: 机器人是否可设置聊天表情包，仅在使用 get_chat 方法时返回

    :类型: ``Optional[bool]``
    """
    linked_chat_id: Optional[int]
    """
    :说明: 链接到的聊天的 id，仅在使用 get_chat 方法时返回

    :类型: ``Optional[int]``
    """
    location: Optional["ChatLocation"]
    """
    :说明: 聊天地址，仅在使用 get_chat 方法时返回

    :类型: ``Optional[ChatLocation]``
    """


class Message_(BaseModel):
    message_id: int
    from_: Optional[User] = Field(default=None, alias="from")
    sender_chat: Optional[Chat]
    date: int
    chat: "Chat"
    forward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional["Message_"]
    via_bot: Optional[User]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]
    entities: Optional[List["MessageEntity"]]
    animation: Optional["Animation"]
    audio: Optional["Audio"]
    document: Optional["Document"]
    photo: Optional[List["PhotoSize"]]
    sticker: Optional["Sticker"]
    video: Optional["Video"]
    video_note: Optional["VideoNote"]
    voice: Optional["Voice"]
    caption: Optional[str]
    caption_entities: Optional[List["MessageEntity"]]
    contact: Optional["Contact"]
    dice: Optional["Dice"]
    game: Optional["Game"]
    poll: Optional["Poll"]
    venue: Optional["Venue"]
    location: Optional["Location"]
    new_chat_members: Optional[List[User]]
    left_chat_member: Optional[User]
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List["PhotoSize"]]
    delete_chat_photo: Optional[Literal[True]]
    group_chat_created: Optional[Literal[True]]
    supergroup_chat_created: Optional[Literal[True]]
    channel_chat_created: Optional[Literal[True]]
    message_auto_delete_timer_changed: Optional["MessageAutoDeleteTimerChanged"]
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    pinned_message: Optional["Message_"]
    invoice: Optional["Invoice"]
    successful_payment: Optional["SuccessfulPayment"]
    connected_website: Optional[str]
    passport_data: Optional["PassportData"]
    proximity_alert_triggered: Optional["ProximityAlertTriggered"]
    voice_chat_scheduled: Optional["VoiceChatScheduled"]
    voice_chat_started: Optional["VoiceChatStarted"]
    voice_chat_ended: Optional["VoiceChatEnded"]
    voice_chat_participants_invited: Optional["VoiceChatParticipantsInvited"]
    reply_markup: Optional["InlineKeyboardMarkup"]


class MessageId(BaseModel):
    message_id: int


class MessageEntity(BaseModel):
    type: str
    offset: int
    length: int
    url: Optional[str]
    user: Optional[User]
    language: Optional[str]


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int]


class Animation(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Audio(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    performer: Optional[str]
    title: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]
    thumb: Optional[PhotoSize]


class Document(BaseModel):
    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Video(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class VideoNote(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize]
    file_size: Optional[int]


class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str]
    file_size: Optional[int]


class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str]
    user_id: Optional[int]
    vcard: Optional[str]


class Dice(BaseModel):
    emoji: str
    value: int


class PollOption(BaseModel):
    text: str
    voter_count: int


class PollAnswer(BaseModel):
    poll_id: str
    user: User
    option_ids: List[int]


class Poll(BaseModel):
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int]
    explanation: Optional[str]
    explanation_entities: Optional[List[MessageEntity]]
    open_period: Optional[int]
    close_date: Optional[int]


class Location(BaseModel):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float]
    live_period: Optional[int]
    heading: Optional[int]
    prpximity_alert_radius: Optional[int]


class Venue(BaseModel):
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    google_place_id: Optional[str]
    google_place_type: Optional[str]


class ProximityAlertTriggered(BaseModel):
    traveler: User
    watcher: User
    distance: int


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int


class VoiceChatScheduled(BaseModel):
    start_date: int


class VoiceChatStarted(BaseModel):
    pass


class VoiceChatEnded(BaseModel):
    duration: int


class VoiceChatParticipantsInvited(BaseModel):
    users: Optional[List[User]]


class UserProfilePhotos(BaseModel):
    total_count: int
    photos: List[List[PhotoSize]]


class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int]
    file_path: Optional[str]


class KeyboardButtonPollType(BaseModel):
    type: Optional[str]


class KeyboardButton(BaseModel):
    text: str
    request_contact: Optional[bool]
    request_location: Optional[bool]
    request_poll: Optional[KeyboardButtonPollType]


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]]
    resize_keyboard: Optional[bool]
    one_time_keyboard: Optional[bool]
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool = True
    selective: Optional[bool]


class LoginUrl(BaseModel):
    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class InlineKeyboardButton(BaseModel):
    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl]
    callback_date: Optional[str]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]
    callback_game: Optional["CallbackGame"]
    pay: Optional[bool]


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]]


class CallbackQuery(BaseModel):
    id: str
    from_: Optional[User] = Field(default=None, alias="from")
    message: Optional[Message_]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    date: Optional[str]
    game_short_name: Optional[str]


class ForceReply(BaseModel):
    force_reply: bool = True
    input_field_placeholder: Optional[str]
    selective: Optional[bool]


class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatInviteLink(BaseModel):
    invite_link: str
    creator: User
    is_primary: bool
    is_revoked: bool
    expire_date: Optional[int]
    member_limit: Optional[int]


class ChatMember(BaseModel):
    status: str
    user: User


class ChatMemberOwner(ChatMember):
    status: str = "creator"
    is_anonymous: bool
    custom_title: str


class ChatMemberAdministrator(ChatMember):
    status: str = "administrator"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_voice_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool]
    can_edit_messages: Optional[bool]
    can_pin_messages: Optional[bool]
    custom_title: Optional[str]


class ChatMemberMember(ChatMember):
    status: str = "member"


class ChatMemberRestricted(ChatMember):
    status: str = "restricted"
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int


class ChatMemberLeft(ChatMember):
    status: str = "left"


class ChatMemberBanned(ChatMember):
    status: str = "kicked"


class ChatMemberUpdated(BaseModel):
    chat: Chat
    from_: User = Field(alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]


class ChatLocation(BaseModel):
    location: Location
    address: str


class BotCommand(BaseModel):
    command: str
    description: str


class BotCommandScope(BaseModel):
    type: str


class BotCommandScopeDefault(BotCommandScope):
    type: str = "default"


class BotCommandScopeAllPrivateChats(BotCommandScope):
    type: str = "all_private_chats"


class BotCommandScopeAllGroupChats(BotCommandScope):
    type: str = "all_group_chats"


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    type: str = "all_chat_administrators"


class BotCommandScopeChat(BotCommandScope):
    type: str = "chat"
    chat_id: Union[int, str]


class BotCommandScopeChatAdministrators(BotCommandScope):
    type: str = "chat_administrators"
    chat_id: Union[int, str]


class BotCommandScopeChatMember(BotCommandScope):
    type: str = "chat_member"
    chat_id: Union[int, str]
    user_id: int


class ResponseParameters(BaseModel):
    migrate_to_chat_id: Optional[int]
    retry_after: Optional[int]


class InputFile(BaseModel):
    pass


class InputMedia(BaseModel):
    type: str
    media: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]


class InputMediaPhoto(InputMedia):
    type: str = "photo"


class InputMediaVideo(InputMedia):
    type: str = "video"
    thumb: Optional[Union[InputFile, str]]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]
    supports_streaming: Optional[bool]


class InputMediaAnimation(InputMedia):
    type: str = "animation"
    thumb: Optional[Union[InputFile, str]]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]


class InputMediaAudio(InputMedia):
    type: str = "audio"
    thumb: Optional[Union[InputFile, str]]
    duration: Optional[int]
    performer: Optional[str]
    title: Optional[str]


class InputMediaDocument(InputMedia):
    type: str = "document"
    thumb: Optional[Union[InputFile, str]]
    disable_content_type_detection: Optional[bool]


class MaskPosition(BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class Sticker(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSize]
    emoji: Optional[str]
    set_name: Optional[str]
    mask_position: Optional[MaskPosition]
    file_size: Optional[int]


class StickerSet(BaseModel):
    name: str
    title: str
    is_animated: bool
    contains_masks: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSize]


class InlineQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    query: str
    offset: str
    chat_type: Optional[str]
    Location: Optional[Location]


class InputMessageContent(BaseModel):
    pass


class InputTextMessageContent(InputMessageContent):
    message_text: str
    parse_mode: Optional[str]
    entities: Optional[List[MessageEntity]]
    disable_web_page_preview: Optional[bool]


class InputLocationMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    horizontal_accuracy: Optional[float]
    live_period: Optional[int]
    heading: Optional[int]
    prpximity_alert_radius: Optional[int]


class InputVenueMessageContent(InputMessageContent):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    google_place_id: Optional[str]
    google_place_type: Optional[str]


class InputContactMessageContent(InputMessageContent):
    phone_number: str
    first_name: str
    last_name: Optional[str]
    vcard: Optional[str]


class InputInvoiceMessageContent(InputMessageContent):
    title: str
    description: str
    payload: str
    provider_token: str
    currency: str
    prices: List["LabeledPrice"]
    max_tip_amount: Optional[int]
    suggested_tip_amounts: Optional[List[int]]
    provider_data: Optional[str]
    photo_url: Optional[str]
    photo_size: Optional[int]
    photo_width: Optional[int]
    photo_height: Optional[int]
    need_name: Optional[bool]
    need_phone_number: Optional[bool]
    need_email: Optional[bool]
    need_shipping_address: Optional[bool]
    send_phone_number_to_provider: Optional[bool]
    send_email_to_provider: Optional[bool]
    is_flexible: Optional[bool]


class InlineQueryResult(BaseModel):
    type: str
    id: str
    reply_markup: Optional[InlineKeyboardMarkup]


class InlineQueryResultArticle(InlineQueryResult):
    type: str = "article"
    title: str
    input_message_content: InputMessageContent
    url: Optional[str]
    hide_url: Optional[bool]
    description: Optional[str]
    thumb_url: Optional[str]
    thumb_width: Optional[int]
    thumb_height: Optional[int]


class InlineQueryResultPhoto(InlineQueryResult):
    type: str = "photo"
    photo_url: str
    thumb_url: str
    photo_width: Optional[int]
    photo_height: Optional[int]
    title: Optional[str]
    description: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultGif(InlineQueryResult):
    type: str = "gif"
    gif_url: str
    gif_width: Optional[int]
    gif_height: Optional[int]
    gif_duration: Optional[int]
    thumb_url: str
    thumb_mime_type: Optional[str]
    title: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    type: str = "mpeg4_gif"
    mpeg4_url: str
    mpeg4_width: Optional[int]
    mpeg4_height: Optional[int]
    mpeg4_duration: Optional[int]
    thumb_url: str
    thumb_mime_type: Optional[str]
    title: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultVideo(InlineQueryResult):
    type: str = "video"
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    video_width: Optional[int]
    video_height: Optional[int]
    video_duration: Optional[int]
    description: Optional[str]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultAudio(InlineQueryResult):
    type: str = "audio"
    audio_url: str
    title: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    performer: Optional[str]
    audio_duration: Optional[int]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultVoice(InlineQueryResult):
    type: str = "voice"
    voice_url: str
    title: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    voice_duration: Optional[int]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultDocument(InlineQueryResult):
    type: str = "document"
    title: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    document_url: str
    mime_type: str
    description: Optional[str]
    input_message_content: Optional[InputMessageContent]
    thumb_url: Optional[str]
    thumb_width: Optional[int]
    thumb_height: Optional[int]


class InlineQueryResultLocation(InlineQueryResult):
    type: str = "location"
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: Optional[float]
    live_period: Optional[int]
    heading: Optional[int]
    prpximity_alert_radius: Optional[int]
    input_message_content: Optional[InputMessageContent]
    thumb_url: Optional[str]
    thumb_width: Optional[int]
    thumb_height: Optional[int]


class InlineQueryResultVenue(InlineQueryResult):
    type: str = "venue"
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    google_place_id: Optional[str]
    google_place_type: Optional[str]
    input_message_content: Optional[InputMessageContent]
    thumb_url: Optional[str]
    thumb_width: Optional[int]
    thumb_height: Optional[int]


class InlineQueryResultContact(InlineQueryResult):
    type: str = "contact"
    phone_number: str
    first_name: str
    last_name: Optional[str]
    user_id: Optional[int]
    vcard: Optional[str]
    input_message_content: Optional[InputMessageContent]
    thumb_url: Optional[str]
    thumb_width: Optional[int]
    thumb_height: Optional[int]


class InlineQueryResultGame(InlineQueryResult):
    type: str = "game"
    game_short_name: str


class InlineQueryResultCachedPhoto(InlineQueryResult):
    type: str = "photo"
    photo_file_id: str
    title: Optional[str]
    description: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedGif(InlineQueryResult):
    type: str = "gif"
    gif_file_id: str
    title: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):
    type: str = "mpeg4_gif"
    mpeg4_file_id: str
    title: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedSticker(InlineQueryResult):
    type: str = "sticker"
    sticker_file_id: str
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedDocument(InlineQueryResult):
    type: str = "document"
    title: str
    document_file_id: str
    description: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedVideo(InlineQueryResult):
    type: str = "video"
    video_file_id: str
    title: str
    description: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedVoice(InlineQueryResult):
    type: str = "voice"
    voice_file_id: str
    title: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class InlineQueryResultCachedAudio(InlineQueryResult):
    type: str = "audio"
    audio_file_id: str
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    input_message_content: Optional[InputMessageContent]


class ChosenInlineResult(BaseModel):
    result_id: str
    from_: User = Field(alias="from")
    Location: Optional[Location]
    inline_message_id: Optional[str]
    query: str


class LabeledPrice(BaseModel):
    label: str
    amount: int


class Invoice(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    shipping_address: Optional[ShippingAddress]


class ShippingOption(BaseModel):
    id: str
    title: str
    prices: List[LabeledPrice]


class SuccessfulPayment(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class ShippingQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]


class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(BaseModel):
    type: str
    data: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    files: Optional[List[PassportFile]]
    front_side: Optional[PassportFile]
    reverse_side: Optional[PassportFile]
    selfie: Optional[PassportFile]
    translation: Optional[List[PassportFile]]
    hash: str


class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secert: str


class PassportElementError(BaseModel):
    source: str
    type: str
    message: str


class PassportElementErrorDataField(PassportElementError):
    source: str = "data"
    field_name: str
    data_hash: str


class PassportElementErrorFrontSide(PassportElementError):
    source: str = "front_side"
    file_hash: str


class PassportElementErrorReverseSide(PassportElementError):
    source: str = "reverse_side"
    file_hash: str


class PassportElementErrorSelfie(PassportElementError):
    source: str = "selfie"
    file_hash: str


class PassportElementErrorFile(PassportElementError):
    source: str = "file"
    file_hash: str


class PassportElementErrorFiles(PassportElementError):
    source: str = "files"
    file_hashes: List[str]


class PassportElementErrorTranslationFile(PassportElementError):
    source: str = "translation_file"
    file_hash: str


class PassportElementErrorTranslationFiles(PassportElementError):
    source: str = "translation_files"
    file_hashes: List[str]


class PassportElementErrorUnspecified(PassportElementError):
    source: str = "unspecified"
    element_hash: str


class PassportData(BaseModel):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials


class Game(BaseModel):
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str]
    text_entities: Optional[List[MessageEntity]]
    animation: Optional[Animation]


class CallbackGame(BaseModel):
    pass


class GameHighScore(BaseModel):
    position: int
    user: User
    score: int


# 动态语言的悲哀
Update.update_forward_refs()
Chat.update_forward_refs()
Message_.update_forward_refs()
InlineKeyboardButton.update_forward_refs()
