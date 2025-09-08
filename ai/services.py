"""
AI Services for FreelanceHub Platform
Using OpenAI API for smart features
"""

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


class AIJobAssistant:
    @staticmethod
    def generate_job_description(title, skills, budget_range, description_brief):
        """
        Generate a professional job description using OpenAI
        """
        try:
            prompt = f"""
            Create a professional and attractive job posting for a freelance project:
            
            Job Title: {title}
            Required Skills: {skills}
            Budget Range: {budget_range}
            Brief Description: {description_brief}
            
            Please create:
            1. An engaging job title (if current one can be improved)
            2. A clear project description
            3. Specific requirements and deliverables
            4. Preferred freelancer qualifications
            5. Project timeline expectations
            
            Make it professional, clear, and likely to attract quality freelancers.
            """

            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional job posting expert for freelance platforms.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS_JOB_DESCRIPTION,
                temperature=settings.OPENAI_TEMPERATURE,
            )

            return {
                "success": True,
                "generated_description": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "generated_description": None}


class AIProposalAssistant:
    @staticmethod
    def generate_proposal(job_description, freelancer_bio, freelancer_skills):
        """
        Generate a personalized proposal for a freelancer
        """
        try:
            prompt = f"""
            Write a winning freelance proposal based on:
            
            Job Description: {job_description}
            My Bio: {freelancer_bio}
            My Skills: {freelancer_skills}
            
            Create a proposal that:
            1. Shows understanding of the project
            2. Highlights relevant experience
            3. Explains my approach
            4. Demonstrates value
            5. Includes a professional closing
            
            Keep it concise, professional, and personalized.
            """

            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert freelance proposal writer.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS_PROPOSAL,
                temperature=settings.OPENAI_TEMPERATURE,
            )

            return {
                "success": True,
                "generated_proposal": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "generated_proposal": None}


class AIPlatformAssistant:
    @staticmethod
    def get_platform_help(user_question, user_type="freelancer"):
        """
        Provide platform guidance and help
        """
        try:
            context = "FreelanceHub is a platform connecting freelancers with clients for project-based work."

            prompt = f"""
            User Type: {user_type}
            Question: {user_question}
            Platform: {context}
            
            Provide helpful, specific guidance for this user's question about using the freelance platform.
            Be concise and actionable.
            """

            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for a freelance platform.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS_ASSISTANT,
                temperature=settings.OPENAI_ASSISTANT_TEMPERATURE,
            )

            return {
                "success": True,
                "response": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "I'm sorry, I'm having trouble right now. Please try again later.",
            }
