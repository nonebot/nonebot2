from typing import List, Optional, Union

from nonebot.adapters import Bot as BaseBot

from .model import *

class Bot(BaseBot):
    async def get_updates(
        self,
        offset: Optional[int],
        limit: Optional[int],
        timeout: Optional[int],
        allowed_updates: Optional[List[str]],
    ): ...
    async def set_webhook(
        self,
        url: str,
        certificate: Optional[InputFile],
        ip_address: Optional[str],
        max_connections: Optional[int],
        allowed_updates: Optional[List[str]],
        drop_pending_updates: Optional[bool],
    ): ...
    async def delete_webhook(self, drop_pending_updates: Optional[bool]): ...
    async def get_webhook_info(self): ...
    async def get_me(self):
        """
        :说明:
          用于测试机器人 Token 的 API
        :返回:
          * ``User``: 机器人本身的 User
        """
        ...
    async def log_out(self): ...
    async def close(self): ...
    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str],
        entities: Optional[List[MessageEntity]],
        disble_web_page_preview: Optional[bool],
        disble_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        diable_notification: Optional[bool],
        message_id: int,
    ): ...
    async def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        duration: Optional[int],
        performer: Optional[str],
        title: Optional[str],
        thumb: Optional[Union[InputFile, str]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[InputFile, str],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        disable_content_type_detection: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[InputFile, str],
        duration: Optional[int],
        width: Optional[int],
        height: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        support_streaming: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[InputFile, str],
        duration: Optional[int],
        width: Optional[int],
        height: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[InputFile, str],
        caption: Optional[str],
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        duration: Optional[int],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[InputFile, str],
        duration: Optional[int],
        length: Optional[int],
        thumb: Optional[Union[InputFile, str]],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_media_group(
        self,
        chat_id: Union[int, str],
        media: List[
            Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]
        ],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
    ): ...
    async def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        horizontal_accurary: Optional[float],
        live_period: Optional[int],
        heading: Optional[int],
        proximity_alert_radius: Optional[int],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def edit_message_live_location(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[int],
        latitude: float,
        longitude: float,
        horizontal_accurary: Optional[float],
        heading: Optional[int],
        proximity_alert_radius: Optional[int],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def stop_message_live_location(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[int],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str],
        foursquare_type: Optional[str],
        google_place_id: Optional[str],
        google_place_type: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: Optional[str],
        vcard: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        is_anonymous: Optional[bool],
        type: Optional[str],
        allows_multiple_answers: Optional[bool],
        correct_option_id: Optional[int],
        explanation: Optional[str],
        explanation_parse_mode: Optional[str],
        explanation_entities: Optional[List[MessageEntity]],
        open_period: Optional[int],
        close_date: Optional[int],
        is_closed: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_dice(
        self,
        chat_id: Union[int, str],
        emoji: Optional[str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def send_chat_action(self, chat_id: Union[int, str], action: str): ...
    async def get_user_profile_photos(
        self, user_id: int, offset: Optional[int], limit: Optional[int]
    ): ...
    async def get_file(self, file_id: str): ...
    async def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[int],
        revoke_messages: Optional[bool],
    ): ...
    async def unban_chat_member(
        self, chat_id: Union[int, str], user_id: int, only_if_banned: Optional[bool]
    ): ...
    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        is_anonymous: Optional[bool],
        can_manage_chat: Optional[bool],
        can_post_messages: Optional[bool],
        can_edit_messages: Optional[bool],
        can_delete_messages: Optional[bool],
        can_manage_voice_chats: Optional[bool],
        can_restrict_members: Optional[bool],
        can_promote_members: Optional[bool],
        can_change_info: Optional[bool],
        can_invite_users: Optional[bool],
        can_pin_messages: Optional[bool],
    ): ...
    async def set_chat_adminstrator_custom_title(
        self, chat_id: Union[int, str], user_id: int, custom_title: str
    ): ...
    async def set_chat_permissions(
        self, chat_id: Union[int, str], permissions: ChatPermissions
    ): ...
    async def export_chat_invite_link(self, chat_id: Union[int, str]): ...
    async def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        expire_date: Optional[int],
        member_limit: Optional[int],
    ): ...
    async def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        expire_date: Optional[int],
        member_limit: Optional[int],
    ): ...
    async def revoke_chat_invite_link(
        self, chat_id: Union[int, str], invite_link: str
    ): ...
    async def set_chat_photo(self, chat_id: Union[int, str], photo: InputFile): ...
    async def delete_chat_photo(self, chat_id: Union[int, str]): ...
    async def set_chat_title(self, chat_id: Union[int, str], title: str): ...
    async def set_chat_description(
        self, chat_id: Union[int, str], description: Optional[str]
    ): ...
    async def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        disble_notification: Optional[bool],
    ): ...
    async def unpin_chat_message(
        self, chat_id: Union[int, str], message_id: Optional[int]
    ): ...
    async def unpin_all_chat_messages(self, chat_id: Union[int, str]): ...
    async def leave_chat(self, chat_id: Union[int, str]): ...
    async def get_chat(self, chat_id: Union[int, str]): ...
    async def get_chat_administrators(self, chat_id: Union[int, str]): ...
    async def get_chat_member_count(self, chat_id: Union[int, str]): ...
    async def get_chat_member(self, chat_id: Union[int, str], user_id: int): ...
    async def set_chat_sticker_set(
        self, chat_id: Union[int, str], sticker_set_name: str
    ): ...
    async def delete_chat_sticker_set(self, chat_id: Union[int, str]): ...
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str],
        show_alert: Optional[bool],
        url: Optional[str],
        cache_time: Optional[int],
    ): ...
    async def set_my_commands(
        self,
        commands: List[BotCommand],
        scope: Optional[BotCommandScope],
        language_code: Optional[str],
    ): ...
    async def delete_my_commands(
        self, scope: Optional[BotCommandScope], language_code: Optional[str]
    ): ...
    async def get_my_commands(
        self, scope: Optional[BotCommandScope], language_code: Optional[str]
    ): ...
    async def edit_message_text(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        text: str,
        parse_mode: Optional[str],
        entities: Optional[List[MessageEntity]],
        diable_web_page_preview: Optional[bool],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def edit_message_caption(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        caption: str,
        parse_mode: Optional[str],
        caption_entities: Optional[List[MessageEntity]],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def edit_message_media(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        media: InputMedia,
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def edit_message_reply_markup(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        inline_message_id: Optional[str],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def stop_poll(
        self,
        chat_id: Optional[Union[int, str]],
        message_id: Optional[int],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def delete_message(
        self, chat_id: Optional[Union[int, str]], message_id: Optional[int]
    ): ...
    async def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[InputFile, str],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[
            Union[
                InlineKeyboardMarkup,
                ReplyKeyboardMarkup,
                ReplyKeyboardRemove,
                ForceReply,
            ]
        ],
    ): ...
    async def get_sticker_set(self, name: str): ...
    async def upload_sticker_file(self, user_id: int, png_sticker: InputFile): ...
    async def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        png_sticker: Optional[Union[InputFile, str]],
        tgs_sticker: Optional[InputFile],
        emojis: str,
        contains_masks: Optional[bool],
        mask_potion: Optional[MaskPosition],
    ): ...
    async def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        png_sticker: Optional[Union[InputFile, str]],
        tgs_sticker: Optional[InputFile],
        emojis: str,
        mask_potion: Optional[MaskPosition],
    ): ...
    async def set_sticker_positon_in_set(self, sticker: str, positon: int): ...
    async def delete_sticker_from_set(self, sticker: str): ...
    async def set_sticker_set_thumb(
        self, name: str, user_id: int, thumb: Optional[Union[InputFile, str]]
    ): ...
    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: List[InlineQueryResult],
        cache_time: Optional[int],
        is_persional: Optional[bool],
        next_offset: Optional[str],
        switch_pm_text: Optional[str],
        switch_pm_parameter: Optional[str],
    ): ...
    async def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        provider_token: str,
        prices: List[LabeledPrice],
        max_tip_amount: Optional[int],
        suggested_tip_amounts: Optional[int],
        start_parameter: Optional[str],
        provider_date: Optional[str],
        photo_url: Optional[str],
        photo_size: Optional[int],
        photo_width: Optional[int],
        photo_height: Optional[int],
        need_name: Optional[bool],
        need_phone_number: Optional[bool],
        need_email: Optional[bool],
        need_shipping_address: Optional[bool],
        send_phone_number_to_provider: Optional[bool],
        send_email_to_provider: Optional[bool],
        is_flexible: Optional[bool],
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[List[ShippingOption]],
        error_message: Optional[str],
    ): ...
    async def answer_pre_checkout_query(
        self, pre_checkout_query_id: str, ol: bool, error_message: Optional[str]
    ): ...
    async def set_passport_data_errors(
        self, user_id: int, errors: List[PassportElementError]
    ): ...
    async def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        diable_notification: Optional[bool],
        reply_to_message_id: Optional[int],
        allow_sending_without_reply: Optional[bool],
        reply_markup: Optional[InlineKeyboardMarkup],
    ): ...
    async def set_game_score(
        self,
        user_id: int,
        score: int,
        force: Optional[bool],
        disable_edit_message: Optional[bool],
        chat_id: Optional[int],
        message_id: Optional[int],
        inline_message_id: Optional[str],
    ): ...
    async def get_game_high_score(
        self,
        user_id: int,
        chat_id: Optional[int],
        message_id: Optional[int],
        inline_message_id: Optional[str],
    ): ...
