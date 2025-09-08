"""
Test configuration for AI services
"""

from django.test import TestCase
from django.conf import settings


class AIConfigurationTest(TestCase):
    """Test AI configuration settings"""

    def test_openai_settings_exist(self):
        """Test that all OpenAI settings are properly configured"""
       
        self.assertTrue(hasattr(settings, "OPENAI_API_KEY"))
        self.assertTrue(hasattr(settings, "OPENAI_MODEL"))
        self.assertTrue(hasattr(settings, "OPENAI_MAX_TOKENS_JOB_DESCRIPTION"))
        self.assertTrue(hasattr(settings, "OPENAI_MAX_TOKENS_PROPOSAL"))
        self.assertTrue(hasattr(settings, "OPENAI_MAX_TOKENS_ASSISTANT"))
        self.assertTrue(hasattr(settings, "OPENAI_TEMPERATURE"))
        self.assertTrue(hasattr(settings, "OPENAI_ASSISTANT_TEMPERATURE"))

    def test_openai_model_default(self):
        """Test that OpenAI model has correct default"""
        self.assertEqual(settings.OPENAI_MODEL, "gpt-3.5-turbo")

    def test_openai_token_limits(self):
        """Test that token limits are within reasonable ranges"""
        self.assertGreater(settings.OPENAI_MAX_TOKENS_JOB_DESCRIPTION, 0)
        self.assertGreater(settings.OPENAI_MAX_TOKENS_PROPOSAL, 0)
        self.assertGreater(settings.OPENAI_MAX_TOKENS_ASSISTANT, 0)
        self.assertLessEqual(settings.OPENAI_MAX_TOKENS_JOB_DESCRIPTION, 1000)

    def test_openai_temperature_ranges(self):
        """Test that temperature values are in valid range (0-2)"""
        self.assertGreaterEqual(settings.OPENAI_TEMPERATURE, 0)
        self.assertLessEqual(settings.OPENAI_TEMPERATURE, 2)
        self.assertGreaterEqual(settings.OPENAI_ASSISTANT_TEMPERATURE, 0)
        self.assertLessEqual(settings.OPENAI_ASSISTANT_TEMPERATURE, 2)
