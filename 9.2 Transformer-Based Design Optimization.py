import torch
import torch.nn as nn
from transformers import GPT2Model, GPT2Config


class BuildingDesignTransformer:
    """Transformer model for building design optimization"""

    def __init__(self):
        self.config = GPT2Config(
            vocab_size=1000,  # Building parameter vocabulary
            n_positions=50,  # Maximum sequence length
            n_embd=256,  # Embedding dimension
            n_layer=8,  # Number of layers
            n_head=8  # Number of attention heads
        )

        self.model = GPT2Model(self.config)
        self.parameter_head = nn.Linear(256, 10)  # Output building parameters
        self.performance_head = nn.Linear(256, 3)  # Output performance metrics

    def forward(self, climate_sequence, site_constraints):
        """Forward pass through transformer"""
        # Combine climate and site data
        input_sequence = torch.cat([climate_sequence, site_constraints], dim=1)

        # Get transformer outputs
        outputs = self.model(inputs_embeds=input_sequence)
        hidden_states = outputs.last_hidden_state

        # Get final representation
        final_hidden = hidden_states[:, -1, :]  # Last token

        # Predict building parameters and performance
        parameters = self.parameter_head(final_hidden)
        performance = self.performance_head(final_hidden)

        return {
            'building_parameters': torch.sigmoid(parameters),  # Normalize to [0,1]
            'predicted_performance': performance
        }

    def optimize_with_attention(self, climate_data, site_data, iterations=10):
        """Use attention mechanism for iterative optimization"""
        current_design = torch.randn(1, 10)  # Random initial design

        for i in range(iterations):
            # Encode current state
            state_embedding = self.encode_design_state(
                current_design, climate_data, site_data
            )

            # Get attention weights to understand what the model focuses on
            with torch.no_grad():
                outputs = self.model(inputs_embeds=state_embedding,
                                     output_attentions=True)
                attention_weights = outputs.attentions[-1]  # Last layer attention

            # Generate improved design
            result = self.forward(climate_data, site_data)
            current_design = result['building_parameters']

            # Log attention patterns for interpretability
            self.log_attention_patterns(attention_weights, i)

        return current_design