from .manager import MatcherManager as MatcherManager
from .provider import DEFAULT_PROVIDER_CLASS as DEFAULT_PROVIDER_CLASS
from .provider import MatcherProvider as MatcherProvider

matchers = MatcherManager()

from .matcher import Matcher as Matcher
from .matcher import MatcherSource as MatcherSource
from .matcher import current_bot as current_bot
from .matcher import current_event as current_event
from .matcher import current_handler as current_handler
from .matcher import current_matcher as current_matcher
