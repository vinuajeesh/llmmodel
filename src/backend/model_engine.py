try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False
    print("WARNING: llama-cpp-python not found. AI features will be mocked.")

import os

class ModelEngine:
    def __init__(self):
        self.model = None
        self.model_path = None

    def load_model(self, model_path):
        if not os.path.exists(model_path):
            return False, "Model file not found."

        try:
            if HAS_LLAMA:
                # n_ctx=2048 is a safe default, can be increased.
                # n_gpu_layers=-1 attempts to offload all to GPU if available.
                self.model = Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=-1, verbose=True)
                self.model_path = model_path
                return True, "Model loaded successfully."
            else:
                self.model_path = model_path
                return True, "Model loaded (MOCK mode)."
        except Exception as e:
            return False, str(e)

    def generate_response(self, messages, system_prompt=None, max_tokens=1024, stream=True):
        """
        messages: list of dicts [{'role': 'user', 'content': '...'}, ...]
        """
        if not self.model and not (not HAS_LLAMA and self.model_path):
            yield "Error: No model loaded."
            return

        # Construct prompt based on ChatML or similar format (simplified here)
        # Ideally, we should use the chat_format parameter in Llama if available,
        # or manually format if we know the model type.
        # Llama-cpp-python has high-level create_chat_completion method.

        if HAS_LLAMA and self.model:
            try:
                # Add system prompt if provided and not already in messages
                msgs_to_send = []
                if system_prompt:
                     msgs_to_send.append({"role": "system", "content": system_prompt})
                msgs_to_send.extend(messages)

                response_iterator = self.model.create_chat_completion(
                    messages=msgs_to_send,
                    max_tokens=max_tokens,
                    stream=stream
                )

                if stream:
                    for chunk in response_iterator:
                        delta = chunk['choices'][0]['delta']
                        if 'content' in delta:
                            yield delta['content']
                else:
                    yield response_iterator['choices'][0]['message']['content']
            except Exception as e:
                yield f"Error generating response: {str(e)}"
        else:
            # Mock response
            import time
            mock_response = f"This is a mock response from the {os.path.basename(self.model_path)} model. I received your messages."
            for word in mock_response.split():
                yield word + " "
                time.sleep(0.05)

    def is_loaded(self):
        return self.model is not None or (not HAS_LLAMA and self.model_path is not None)
