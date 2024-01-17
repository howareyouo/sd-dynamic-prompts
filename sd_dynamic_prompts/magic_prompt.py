from itertools import zip_longest

from dynamicprompts.generators.magicprompt import MagicPromptGenerator

from sd_dynamic_prompts.special_syntax import (
    append_chunks,
    remove_a1111_special_syntax_chunks,
)


class SpecialSyntaxAwareMagicPromptGenerator(MagicPromptGenerator):
    """
    Magic Prompt generator that is aware of A1111 special syntax (LoRA, hypernet, etc.).
    """

    def _generate_magic_prompts(self, orig_prompts: list[str]) -> list[str]:
        orig_prompts, chunks = zip(
            *(remove_a1111_special_syntax_chunks(p) for p in orig_prompts),
        )
        # `transformers` is rather particular that the input is a list, not a tuple
        magic_prompts = super()._generate_magic_prompts(list(orig_prompts))
        # in case we somehow get less magic prompts than we started with,
        # use zip_longest instead of zip.
        return [
            append_chunks(prompt, chunk)
            for prompt, chunk in zip_longest(magic_prompts, chunks, fillvalue=None)
        ]
