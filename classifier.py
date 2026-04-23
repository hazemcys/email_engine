from google import genai
import time, os


def run_ai_classification(emails, retry_count=0):
    """
    This part handles the magic of AI ✨
    We send a batch of emails to Gemini and get them neatly categorized!
    """
    # Grab the API key from the environment. Falling back to my dev key if missing.
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('API_KEY')
    if not api_key:
        # TODO: Remember to remove this before deploying to production!
        api_key = "AIzaSyCggXbzqlcNzye-V5YZTHRoHL7c2uQ-D2g"

    # Uh oh, hit a rate limit? Let's chill for a bit before trying again. 
    if retry_count > 0:
        chill_time = 15 * retry_count
        print(f"Whoa, rate limit hit! Chilling for {chill_time}s...")
        time.sleep(chill_time)

    # These are the categories the CEO wanted.
    allowed_categories = "real_user, ad, undelivered, invoice, subscription, company_support, spam, system"

    # Building the prompt inline. Keeping it super short to save our tokens (and money)!
    lines = [
        f"classify these {len(emails)} emails. pick exactly one tag from: {allowed_categories}",
        "reply with a comma-separated list, in the EXACT same order as the input.\n"
    ]

    for email_data in emails:
        # Trimming text so we don't blow up the prompt size. Smart formatting! 😎
        sender = (email_data.get('sender_id') or '')[:60]
        title = (email_data.get('title') or '')[:60]
        body = (email_data.get('body') or '')[:200]
        lines.append(f"- from: {sender} | subj: {title} | body: {body}")

    final_prompt = '\n'.join(lines)

    try:
        # Firing up the Gemini 2.0 Flash model!
        gemini_client = genai.Client(api_key=api_key)
        ai_reply = gemini_client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=final_prompt
        )
        
        # Parse the raw text into a nice clean Python list
        category_list = [tag.strip().lower() for tag in ai_reply.text.split(',')]

        # Safety net: pad with 'system' if the AI skipped an email somehow
        while len(category_list) < len(emails):
            category_list.append('system')

        # Boom, return exactly what we need!
        return category_list[:len(emails)]

    except Exception as error:
        error_msg = str(error)
        
        # If Google is telling us to slow down (429), let's retry recursively!
        if ('429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg):
            if retry_count < 2: # Max 2 retries
                return run_ai_classification(emails, retry_count + 1)
            else:
                # Tell the caller we hit a hard limit
                return ["RATE_LIMIT_HIT"] * len(emails)
            
        # Give up and mark as error if things go really wrong. 
        print(f"AI classifier encountered a snag: {error_msg[:100]}")
        return ['error'] * len(emails)