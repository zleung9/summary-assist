def prompt_for_long_summary(text, n_words=200):
        """
        Provide a group of prompt messages for generating a long summary for a news article.

        Parameters:
        ----------
        n_words : int
            Number of words to summarize to, by default 200.

        Returns:
        ----------
        list
            A list of prompt messages in the format of dictionaries with 'role' and 'content' keys.

        Notes:
        ------
        The prompt messages are designed to generate JSON output.
        """
        prompt =  [
            {
                "role": "system", 
                "content": f"You are a professional news reporter. You are specific about numbers."
            },
            {
                "role": "user",
                "content": "Summarize the given news article in json format. Let's do it step by step:\n1. The output JSON consists two fields: 'title', 'summary' and 'country', where the 'title field' is the title of the summary and the 'summary' field is the summary itself. \n2. Summarize the article with {n_words} words or less. \n3. Put the summary in the 'summary' field of the output. \n4. Add a title for the news, and put the title in the 'title' field of the output. \n4. Infer the country where the news occurred and add it to the 'country' field of the output."
            },
            {
                "role": "user", 
                "content": f"Pay attention to the content of the news artile. If the news is about a technology or research, please briefly describe the technology or research in the article. If the news is about a company raising a certain amount of money from investors. Please include the raised amount and the leading investor both in the title and the summary. Please also include other participating investors, as well as the purpose of the fundraising if any, in the summary. Please be specific about numbers."
            },
            {
                "role": "user", 
                "content": f"Here is the news article you are to summarize: \n{text}"},
        ]
        return prompt


def prompt_for_short_summary(text, n_words=50):
        """
        Provide a group of prompt messages for generating a concise summary for a news article.

        Parameters:
        ----------
        n_words : int
            Number of words to summarize to, by default 50.

        Returns:
        ----------
        list
            A list of prompt messages in the format of dictionaries with 'role' and 'content' keys.
        
        Notes:
        ------
        The prompt messages are designed to generate text output (not JSON).
        """
        prompt =  [
            {
                "role": "system", 
                "content": f"You are a professional news reporter. You are specific about numbers."
            },
            {
                "role": "user",
                "content": "Summarize the following article and make sure the length of the summary is {n_words} words or less. "
            },
            {
                "role": "user", 
                "content": f"Please focus on the event itself. If the article is about a technology or research, please briefly describe the technology or research in the article. If the news is about a company raising a certain amount of money from investors. Please include the raised amount, the leading investor and other participating investor, as well as the purpose of the fundraising if any. Please be specific about numbers."
            },
            {
                "role": "user", 
                "content": f"Here is the news article you are to summarize: \n{text}"},
        ]
        return prompt

