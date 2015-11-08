import logging
from lazy import lazy


from xblock.core import XBlock
from xblock.fields import Scope, Float, Integer, String
from xblock.fragment import Fragment
from xblock.validation import ValidationMessage
import uuid




class Answer(XBlock):
    @property
    def _get_student_id(self):
        try:
            return self.runtime.anonymous_student_id
        except AttributeError:
            return self.scope_ids.user_id



