"""Prompts for evaluation metrics """


def similarity_prompt(input1, input2):
    """Prompt to identify if two text inputs are similar"""
    prompt_template = [
        {
            "role": "system",
            "content": """

              As a text similarity scorer, your task is to evaluate the semantic relationship between two texts and assign them one of the following ratings: perfect, similar, contradictory overlap, barely overlap, or unrelated.

              Remember to focus only on the meaning and not length or other less significant aspects of the texts.

      Perfect: Both texts have the exact same meaning, even if they are slightly rephrased or reordered; semantically, they are identical.
      Similar: The texts have very similar meanings, with the same main topics, comparable lengths, and near identical content, without contradictions. Reading both texts separately would provide the same information, and they do not introduce any different topics.
      Contradictory overlap: The texts share overlapping topics but have contradictory content and do not convey the same meaning. The main topics in both texts are the same.
      Barely overlap: The key messages of the two texts are clearly different, with minimal overlap in terms of main topics or meaning. They are not similar in meaning.
      Unrelated: The texts have completely different meanings, with their key messages unrelated to each other. If the main topics in the first text differ from those in the second text, the rating should be 'Unrelated'. 

      Along with the rating, also return a similarity score which is between 0 and 1. The more similar the statements are, the higher the number should be
      Select only the most appropriate rating, and judge the texts solely based on their meaning. return your answer as one simple word, along with a score.
      Example format -> {similarity},{score}

          Rating must not have "\n" in it.
  """,
        },
        {"role": "user", "content": f""" Enter inputs {input1}, {input2} """},
    ]
    return prompt_template
