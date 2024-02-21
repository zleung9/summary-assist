def prompt_summary(text, n_words=200):
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
                "content": f"Summarize the given news article in json format.The json output consists the following fields: 'title', 'summary', 'company', 'investors' and 'country'. The value for 'investors' field is a list of strings if not empty. Let's do it step by step:\n" 
            },
            {
                "role": "user",
                "content": f"Step 1. Summarize the article with up to {n_words} words. Put the summary in the 'summary' field of the output. Pay attention to the content of the news artile. If the news is about a technology or research, please briefly describe the technology or research in the article. If the news is about a company raising a certain amount of money from investors. Please mention the raised amount, the leading investor and other participating investors. Please also include the purpose of the fundraising if any. Please be specific about numbers. If the news is about a company going public, please mention the company and the stock exchange it is listed on."
            },
            {
                "role": "user",
                "content": f"Step 3. Find the main company the news is about and add it to the 'company' field of the output, otherwise leave it an empty string."
            },
            {
                "role": "user",
                "content": f"Step 4. Find the investors involved in the news and add them to the 'investors' field of the output, otherwise leave it an empty list. If the news is about funding from DOE (Department of Energy) , treat DOE as investors."
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


def prompt_short_summary(text, n_words=60):
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
                "content": f"Summarize the given news article in json format.The json output consists the following fields: 'title', 'summary', 'company', 'investors' and 'country'. The value for all the fields are set to an empty string. Let's do it step by step:\n" 
            },
            {
                "role": "user",
                "content": f"Step 1. Summarize the article. Please make sure the summary is concise and that the length of the summary does not exceed {n_words} words." 
            },
            {
                "role": "user",
                "content": f"Step 2. Put the summary in the 'summary' field of the output."      
            },
            {
                "role": "user",
                "content": f"Here is the news article you are to summarize: \n{text}"
            },
        ]
        return prompt


def prompt_translate_Chinese(text):
    """
    Provide a group of prompt messages for translating a Chinese text to English.

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
            "content": f"You are an expert news reporter. You are both fluent in Chinese and English. You are designed to take Markdown format as input and output a json format. The 'news' field in the json output is a list of translated news, each news has three field: 'title', 'content' and 'source'."
        },
        {
            "role": "user",
            "content": "You are provided with some text in the form of Markdown. Please translate them into Chinese while maintaining the Markdown style. Let's to it step by step:Also remove the link, instead extract the root url from the link and attached to the end of each paragraph." 
        },
        {
            "role": "user",
            "content": "Step 1, translate the contained text and leave the link as is. Put the main text in the 'content' field."
        },
        {
            "role": "user",
            "content": "Step 2, Make the title bold type in Markdown, and put it in the 'title' field."
        },
        {
            "role": "user",
            "content": "Step 3, Extract root url from the link and put it in the 'source' field."
        },
        {
            "role": "assistant",
            "content": f"Here is an example:\n**CATL Introduces New LFP Batteries.** (*[link](https://www.nextbigfuture.com/2024/01/ev-lfp-battery-price-war-w-55-in-six-months.html)*)\nCATL's new rectangular LFP batteries aim to reach a price of less than $56 per kWh within six months, significantly reducing the current price of $70 per kWh in China. With efforts from China's EV makers, the price is expected to drop to as low as $36 per kWh by next year. Tesla is also projected to save $2000 in battery costs compared to last year.\nThe translated version is: \n**CATL推出新型LFP电池。**\nCATL的新型矩形LFP电池旨在在六个月内达到低于每千瓦时56美元的价格, 显著降低中国目前每千瓦时70美元的价格。在中国电动汽车制造商的努力下, 预计价格将在明年降至低至每千瓦时36美元。特斯拉预计与去年相比可节省2000美元的电池成本。(source: nextbigfuture)"      
        },
        {
            "role": "assistant",
            "content": f"Here is another example:\n**NREL Simulates Sustainable Aviation Fuel Combustion for Industry Support.** ([_link_](https://www.nrel.gov/news/features/2024/on-the-ground-in-colorado-nrel-is-simulating-sustainable-aviation-fuel-combustion-during-flight.html))\n The National Renewable Energy Laboratory (NREL) is supporting the aviation industry in fine-tuning sustainable aviation fuel (SAF) chemistry, crucial for decarbonizing flight. NREL's computational science center is simulating detailed SAF combustion in a 'virtual jet engine,' aiming to provide insights for optimizing safety and performance. This effort may accelerate SAF production and usage, potentially reshaping jet fuel chemistry in the industry.\nThe translated version is:\nNREL模拟支持可持续航空燃料燃烧。\n美国国家可再生能源实验室(NREL)正在支持航空业调优可持续航空燃料(SAF)化学成分,这对于减少飞行碳排放至关重要。NREL的计算科学中心正在模拟详细的SAF燃烧过程,利用“虚拟喷气发动机”,旨在提供有关优化安全性和性能的见解。这一努力可能加速SAF的生产和使用,潜在地重塑行业的喷气燃料化学成分。(source: nrel.gov)" 
        },
        {
            "role": "user",
            "content": f"Please translate the following news into Chinese. Names (such as company, person, location, etc) stay in its original language. Translation should conform to Chinese writing habits.\n\n{text}"
        }
    ]
    return prompt
