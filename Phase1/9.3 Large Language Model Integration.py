from transformers import AutoTokenizer, AutoModelForCausalLM
import openai


class LLMBuildingAssistant:
    """Large Language Model for building design assistance"""

    def __init__(self):
        # Initialize local LLM (alternative to OpenAI)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

        # Building domain knowledge base
        self.knowledge_base = self.load_building_knowledge()

    def generate_design_recommendations(self, climate_analysis, user_preferences):
        """Generate natural language design recommendations"""

        # Create context prompt
        context = f"""
        Climate Analysis:
        - Location: {climate_analysis['location']}
        - Climate Zone: {climate_analysis['climate_zone']}
        - Average Temperature: {climate_analysis['avg_temperature']}°C
        - Solar Potential: {climate_analysis['solar_potential']}%

        User Preferences:
        - Building Type: {user_preferences.get('building_type', 'residential')}
        - Priority: {user_preferences.get('priority', 'energy efficiency')}
        - Budget: {user_preferences.get('budget', 'medium')}

        Based on this information, provide specific architectural recommendations:
        """

        # Generate recommendations using LLM
        recommendations = self.query_llm(context)

        # Parse and structure recommendations
        structured_recommendations = self.parse_recommendations(recommendations)

        return structured_recommendations

    def explain_optimization_results(self, optimization_results):
        """Explain optimization results in natural language"""

        prompt = f"""
        Building Optimization Results:
        - Optimal Orientation: {optimization_results['orientation']}°
        - Window-to-Wall Ratio: {optimization_results['wwr']:.1%}
        - Predicted Energy Consumption: {optimization_results['energy']} kWh/m²/year
        - Estimated Cost: ${optimization_results['cost']:,.2f}

        Explain why these parameters are optimal and what benefits they provide:
        """

        explanation = self.query_llm(prompt)
        return explanation

    def interactive_design_chat(self, user_message, design_context):
        """Interactive chat interface for design questions"""

        # Build conversation context
        conversation_prompt = f"""
        You are an expert building design assistant. The current design context is:

        Building Parameters:
        - Location: {design_context['location']}
        - Type: {design_context['building_type']}
        - Current Design: {design_context['current_design']}

        User Question: {user_message}

        Provide a helpful, technical response:
        """

        response = self.query_llm(conversation_prompt)
        return response

    def query_llm(self, prompt):
        """Query the language model with a prompt"""
        try:
            # Using OpenAI API (replace with local model if preferred)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are an expert building design consultant with deep knowledge of sustainable architecture, energy efficiency, and climate-responsive design."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            # Fallback to local model or cached responses
            return self.fallback_response(prompt)