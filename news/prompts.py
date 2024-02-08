def prompt_for_summary(text):
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
                "content": f"You are a professional news reporter. You are specific about numbers. You are designed to output a json format."
            },
            {
                "role": "user",
                "content": f"Summarize the given news article in json format.The json output consists the following fields: 'title', 'body', 'summary', 'company', 'investors' and 'country'. The value for 'investors' field is a list of strings if not empty. Let's do it step by step:\n" 
            },
            {
                "role": "user",
                "content": f"Step 1. Summarize the article with around 200 words. Put the summary in the 'summary' field of the output. Pay attention to the content of the news artile. If the news is about a technology or research, please briefly describe the technology or research in the article. If the news is about a company raising a certain amount of money from investors. Please mention the raised amount, the leading investor and other participating investors. Please also include the purpose of the fundraising if any. Please be specific about numbers."
            },
            {
                "role": "user",
                "content": f"Step 2. Further summarize the summary produced in step 1 with the same requirement. But in this step please ensure that the length of the summary is does not exceed 50 words. Put the short summary in the 'body' field of the output"
            },
            {
                "role": "user",
                "content": f"Step 3. Find the main company the news is about and add it to the 'company' field of the output, otherwise leave it an empty string."
            },
            {
                "role": "user",
                "content": f"Step 4. Find the investors involved in the news and add them to the 'investors' field of the output, otherwise leave it an empty list."
            },
            {
                "role": "user",
                "content": f"Step 5. Find the country where the news occurred and add it to the 'country' field of the output. Otherwise leave it an empty string."
            },
            {
                "role": "user",
                "content": f"Step 6. Add a title for the news, and put the title in the 'title' field of the output. If it is a fundraising event, please mention the raised amount and the leading investor. An example would be 'ompany X raised Y amount led by investor for ...'"
            },
            {
                "role": "user", 
                "content": f"Here is the news article you are to summarize: \n{text}"
            },
        ]
        return prompt
