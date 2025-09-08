UNCONDITIONAL_DIFF_PROMPT = """
    The following are the result of captioning two groups of images:
    {text}

     I am a machine learning researcher and data scientist trying to build an image classifier. Group A are the captions of the image about the bird class in the training set, and Group B are the test set. I want to figure out what kind of distribution shift there are.

    Please write a list of hypotheses (separated by bullet points "*") of how images from Group A differ from those from Group B via their captions. Each hypothesis should be formatted as "Group A ... and Group B...". For example,
    * "Group A is cars in outdoor environments and Group B is cars in indoor environments.”
    * "Group A is dogs with golden hair and Group B is cats with black hair."
    * "Group A is animals walking around at night and Group B is animals drinking water during the day."
    * "Group A and Group B are similar."

    The answers should be pertaining to the content of the images, not the structure of the captions e.g. "Group A has longer captions and Group B has shorter captions" or "Group A is more detailed and Group B is more general" are incorrect answers.
    
    Again, I want to figure out the main differences between these two groups of images. List properties that holds more often for the images (not captions) in group A compared to group B and vice versa. Your response:
    * "Group A
    """

CAPTION_DIFF_PROMPT = """
    The following are the result of captioning two groups of images:
    {text}

    I am a machine learning researcher and data scientist trying to build an image classifier. Group A are the captions of the image about the bird class in the training set, and Group B are the test set. I want to figure out what kind of distribution shift there are.

    Please write a list of 10 hypotheses (separated by bullet points "*") of how images from Group A differ from those from Group B via their captions. Each hypothesis should be formatted as a tuple of captions, the first aligns more with Group A than not Group B and the second aligns more with Group B and not Group A. For example,
    * ("a photo of a car", "a photo of a car in the snow")
    * ("a photo of a dig", "a photo of a dog with black hair")
    * ("animals walking around", "animals drinking water during the day")
    * ("a photo of an object", "a drawing of an object")
    
    Again, I want to figure out the main differences between these two groups of images. List properties that holds more often for the images in group A compared to group B and vice versa. Your response:
    """

VQA_DIFF_PROMPT = """
    The following are the result of asking a VQA model {question} about the following two groups of captions:

    {text}

    Please write a list of hypotheses (separated by bullet points "-") of how images from
    Group A differ from those from Group B via their captions. Each hypothesis should be formatted as "Group A ... and Group B..." and should be with respect to the caption question. Here are three examples:
    - "Group A is cars in mostly outdoor environments and Group B is cars mostly indoor environments.”
    - "Group A is dogs with golden hair and Group B is cats with black hair."
    - "Group A is various animals walking around at night and Group B is various animals drinking water around during the day."
    - "Group A and Group B are similar."

    The answers should be pertaining to the content of the images, not the structure of the captions. Here are examples of incorrect answers:
    - "Group A has longer captions and Group B has shorter captions"
    - "Group A is more detailed and Group B is more general"
    
    Based on the two caption groups (A and B) from the above...
    """

RUIQI_DIFF_PROMPT = """
    The following are the result of captioning two groups of images:

    {text}

    I am a machine learning researcher trying to build an image classifier. Group A are the captions of the image about a class in the training set, and Group B are the test set. I want to figure out what kind of distribution shift are there.

    Come up with 10 short and distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*") . for example:
    * "dog with a long tail"
    * "sunny"
    * "graphic art"
    * "bird with a brown beak"
    * "blurry"
    * "DSLR photo"
    * "person"

    Do not talk about the caption, e.g., "captions about bird", or "caption with one word", or "detailed caption". Also do not list more than one concept. Here are examples of bad outputs and their corrections:
    * incorrect: "various nature environments like lakes, forests, and mountains" corrected: "nature"
    * incorrect: "images of household object (e.g. bowl, vaccuum, lamp)" corrected: "household objects"
    * incorrect: "Water-related scenes (ocean, river, catamaran)" corrected: "water" or "water-related"
    * incorrect: "people in various settings" corrected: "people"
    * incorrect: "Different types of vehicles including cars, trucks, boats, and RVs" corrected: "vehicles"
    * incorrect: "Images containing wooden elements" corrected: "wooden"

    Again, I want to figure out what kind of distribution shift are there. List properties that holds more often for the images (not captions) in group A compared to group B, with each property being under 5 words. Your response:
"""

RUIQI_DIFF_PROMPT_LONGER_VICUNA = """
    The following are the result of captioning two groups of images:

    {text}

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can better understand my data.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*") . for example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "captions about bird", or "caption with one word", or "detailed caption". Also do not list more than one concept. Here are examples of bad outputs and their corrections:
    * incorrect: "various nature environments like lakes, forests, and mountains" corrected: "nature"
    * incorrect: "images of household object (e.g. bowl, vaccuum, lamp)" corrected: "household objects"
    * incorrect: "Water-related scenes (ocean, river, catamaran)" corrected: "water" or "water-related"
    * incorrect: "Different types of vehicles including cars, trucks, boats, and RVs" corrected: "vehicles"
    * incorrect: "Images involving interaction between humans and animals" corrected: "interaction between humans and animals"
    * incorrect: "More realistic images" corrected: "realistic images"

    Again, I want to figure out what kind of distribution shift are there. List properties that holds more often for the images (not captions) in group A compared to group B. Answer with a list (separated by bullet points "*").
    OUTPUT:
"""

RUIQI_DIFF_PROMPT_LONGER = """
    The following are the result of captioning two groups of images:

    {text}

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can better understand my data.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*") . for example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "captions about bird", or "caption with one word", or "detailed caption". Also do not list more than one concept. Here are examples of bad outputs and their corrections:
    * incorrect: "various nature environments like lakes, forests, and mountains" corrected: "nature"
    * incorrect: "images of household object (e.g. bowl, vaccuum, lamp)" corrected: "household objects"
    * incorrect: "Water-related scenes (ocean, river, catamaran)" corrected: "water" or "water-related"
    * incorrect: "Different types of vehicles including cars, trucks, boats, and RVs" corrected: "vehicles"
    * incorrect: "Images involving interaction between humans and animals" corrected: "interaction between humans and animals"
    * incorrect: "More realistic images" corrected: "realistic images"

    Again, I want to figure out what kind of distribution shift are there. List properties that holds more often for the images (not captions) in group A compared to group B. Answer with a list (separated by bullet points "*"). Your response:
"""

CLIP_FRIENDLY = """
    The following are the result of captioning two groups of images:

    {text}

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can better understand my data.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*"). For example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "caption with one word" and do not list more than one concept. The hypothesis should be a caption, so hypotheses like "more of ...", "presence of ...", "images with ..." are incorrect. Also do not enumerate possibilities within parentheses. Here are examples of bad outputs and their corrections:
    * INCORRECT: "various nature environments like lakes, forests, and mountains" CORRECTED: "nature"
    * INCORRECT: "images of household object (e.g. bowl, vacuum, lamp)" CORRECTED: "household objects"
    * INCORRECT: "Presence of baby animals" CORRECTED: "baby animals"
    * INCORRECT: "Different types of vehicles including cars, trucks, boats, and RVs" CORRECTED: "vehicles"
    * INCORRECT: "Images involving interaction between humans and animals" CORRECTED: "interaction between humans and animals"
    * INCORRECT: "More realistic images" CORRECTED: "realistic images" 
    * INCORRECT: "Insects (cockroach, dragonfly, grasshopper)" CORRECTED: "insects"

    Again, I want to figure out what kind of distribution shift are there. List properties that hold more often for the images (not captions) in group A compared to group B. Answer with a list (separated by bullet points "*"). Your response:
"""

VLM_PROMPT_COT_GPT = """
You are an advanced vision-language model tasked with analyzing two groups of images and identifying differences between them. Your goal is to generate 10 sentences that best describe Group A while being the least applicable to Group B.

### **Instructions:**
1. Analyze the provided descriptions of **Group A** and **Group B**.
2. Identify distinguishing characteristics that are strongly present in **Group A** but absent or weak in **Group B**.
3. Generate concise and clear **descriptive sentences** that:
   - Are strongly representative of **Group A**.
   - Are **not applicable** to **Group B**.
   - Capture **activity, object type, environment, or context** differences.

### **Chain of Thought (CoT) Reasoning Approach:**
To ensure high-quality outputs, follow these reasoning steps:
1. **Identify Core Characteristics:** Examine the most prominent attributes of Group A and Group B.
2. **Find Exclusive Traits:** List features that are **strongly unique** to Group A while being absent or significantly weaker in Group B.
3. **Refine Differences:** Check for ambiguous or overlapping traits and filter them out.
4. **Construct Distinctive Sentences:** Convert the insights into descriptive sentences that best define Group A and **least fit Group B**.

### **Ground Truth Examples:**
- **Group A:** A location where people interact with products and walk around
- **Group B:** A location where people sit and consume prepared items
  - Yes "People moving between various sections, holding selected items."
  - No "People engaged in a shared social experience" (Applies to both)
  
- **Group A:** A region covered in a frozen, reflective material
- **Group B:** A region dominated by fine-grained mineral particles
  - Yes "Elevated surfaces covered in a crystalline white layer."
  - No "Expansive landscapes with distinct textures." (Fits both)

- **Group A:** A group of organic entities moving freely in open air
- **Group B:** A group of mechanical constructs traveling in a structured manner
  - Yes "Clusters of entities maneuvering dynamically with irregular patterns."
  - No "Objects in motion at various altitudes." (Too generic)

### **Output Format:**
Return a list of 10 sentences that strictly describe **Group A** and not **Group B** in the following format:
* "..."
* "..."
* "..."

Response:

"""

VLM_PROMPT_COT = """
This image contains two groups of images. 20 images from Group A are shown in the first two rows, while 20 images from Group B are shown in the last two rows.

I am a machine learning researcher trying to identify the most significant differences between these two groups.

### Step 1: Identify Key Characteristics
Summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group. Use the following format:
- **Group A:** (three characteristics)
- **Group B:** (three characteristics)

### Step 2: Compare and Contrast
Now, based on the characteristics above, determine the key differences between Group A and Group B. Categorize the differences into the following four types:

#### **1. Entities (名詞：物品、人、動物)**
Identify objects, people, or animals that are more common in Group A compared to Group B. Write **2 key differences**.

#### **2. Actions (動詞：動作行為)**
Identify differences in the actions performed by people, animals, or objects. Write **3 key differences**.

#### **3. Attributes (形容詞：顏色、材質、風格)**
Identify key differences in **color, material, artistic style, or other descriptive attributes**. Write **3 key differences**.

#### **4. Environment (地點：背景、場景、環境)**
Identify differences in the scene, background, or location. Write **2 key differences**.

### Step 3: Focus on the Differences
Now, based on the key differences above, generate **N distinct captions** that describe **differences more likely to be true for Group A compared to Group B**. 

#### **Instructions for Generating Differences:**
- The goal is to create **captions that best reflect Group A** while **being as far removed from Group B as possible**.
- **Write exactly {N} captions**, where **{N} is a customizable number**.
- The captions should highlight **features that are unique to Group A** and **unlikely to appear in Group B**.
- Do **not** use vague terms like "presence of ..." or "images with ...".
- Do **not** list multiple concepts within parentheses.
- Each caption should reflect only **one distinct visual concept**. Example formats:
    * "people shopping in a mall"
    * "a dining table in a restaurant"
    * "white roses"
    * "motorcycles on the street"
    * "casual clothing"
    * "a shopping bag"

### **Final Output Format:**
You must generate exactly **{N} distinct hypotheses** that describe differences more likely to be true for Group A compared to Group B.
- Do not leave the list empty.
- If unsure, make reasonable assumptions.
- The output **must** be a list with **{N}** bullet points.

Please return exactly **{N} bullet points**, in the following format:
* "..."
* "..."
* "..."
"""
VLM_PROMPT_COT_V2 = """
This image contains two groups of images. 20 images from Group A are shown in the first two rows, while 20 images from Group B are shown in the last two rows.

I am a machine learning researcher trying to identify the most significant differences between these two groups.

### Step 1: Identify Key Characteristics
Summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group. Use the following format:
- **Group A:** (three characteristics)
- **Group B:** (three characteristics)

### Step 2: Compare and Contrast
Now, based on the characteristics above, determine the key differences between Group A and Group B. **There must be significant and clear differences between Group A and Group B within the following categories:**

#### **1. Entities (Nouns: Objects, People, Animals)**
Identify objects, people, or animals that are more common in Group A compared to Group B. Write **2 key differences**.

**Important Instructions for Entity Comparison:**
1. **The main subject may not necessarily be a person.** Consider all possible objects, animals, or any other prominent elements in the images.
2. **If Group A and Group B contain similar types of entities, you must describe them in more detail to clarify their distinguishing features.** Do not simply list general object types; instead, specify attributes, function, or context to highlight differences.
3. **If the images contain text, use OCR or other methods to extract the text content and use it as a distinguishing factor between Group A and Group B.** The presence, style, language, or content of the text can be used as a basis for differentiation.

#### **2. Actions (Verbs: Human, Animal, or Object Actions)**
Identify differences in the actions performed by people, animals, or objects. Write **3 key differences**.

#### **3. Attributes (Adjectives: Color, Material, Style)**
Identify key differences in **color, material, artistic style, or other descriptive attributes**. Write **3 key differences**.

#### **4. Environment (Locations, Background, Scene)**
Identify differences in the scene, background, or location. Write **2 key differences**.

### Step 3: Focus on the Differences
Now, based on the key differences above, generate **10 distinct captions** that describe **differences more likely to be true for Group A compared to Group B**. These captions should **emphasize characteristics that are more aligned with Group A and as different as possible from Group B**.

#### **Instructions for Generating Differences:**
- The goal is to create **captions that best reflect Group A** while **being as far removed from Group B as possible**.
- **Write exactly 10 captions**, each reflecting a **distinct and specific concept**.
- Focus on features that are **unique to Group A** and **unlikely to appear in Group B**.
- Do **not** use vague terms like "presence of ..." or "images with ...".
- Do **not** list multiple concepts within parentheses.
- Each caption should reflect only **one distinct visual concept**. Example formats:
    * "a group of people walking through a marketplace"
    * "a round wooden table with decorative plates"
    * "brightly colored flowers in a garden"
    * "a row of parked bicycles along a busy road"
    * "a person wearing a patterned summer outfit"
    * "a backpack filled with books"
  
### Final Output Format:
You must generate exactly **10 distinct hypotheses** that describe differences more likely to be true for Group A compared to Group B.
- Do not leave the list empty.
- If unsure, make reasonable assumptions.
- The output **must** be a list with **10** bullet points.

Please return exactly **10 bullet points** in the following format:
* "..."
* "..."
* "..."
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT = """
This image contains two groups of images. 20 images from Group A are shown in the first two rows, while 20 images from Group B are shown in the last two rows.

I am a machine learning researcher trying to identify the most significant differences between these two groups.

### Step 1: Identify Key Characteristics
Summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group. Use the following format:
- **Group A:** (three characteristics)
- **Group B:** (three characteristics)

### Step 2: Compare and Contrast
Now, based on the characteristics above, determine the key differences between Group A and Group B. **There must be significant and clear differences between Group A and Group B within the following categories:**

#### **1. Entities (Nouns: Objects, People, Animals)**
Identify objects, people, or animals that are more common in Group A compared to Group B. Write **2 key differences**.

**Important Instructions for Entity Comparison:**
1. **The main subject may not necessarily be a person.** Consider all possible objects, animals, or any other prominent elements in the images.
2. **If Group A and Group B contain similar types of entities, you must describe them in more detail to clarify their distinguishing features.** Do not simply list general object types; instead, specify attributes, function, or context to highlight differences.
3. **If the images contain text, use OCR or other methods to extract the text content and use it as a distinguishing factor between Group A and Group B.** The presence, style, language, or content of the text can be used as a basis for differentiation.

#### **2. Actions (Verbs: Human, Animal, or Object Actions)**
Identify differences in the actions performed by people, animals, or objects. Write **3 key differences**.

#### **3. Attributes (Adjectives: Color, Material, Style)**
Identify key differences in **color, material, artistic style, or other descriptive attributes**. Write **3 key differences**.

#### **4. Environment (Locations, Background, Scene)**
Identify differences in the scene, background, or location. Write **2 key differences**.

### Step 3: Focus on the Differences
Now, based on the key differences above, generate **10 distinct captions** that describe **differences more likely to be true for Group A compared to Group B**. These captions should **emphasize characteristics that are more aligned with Group A and as different as possible from Group B**.

#### **Instructions for Generating Differences:**
- The goal is to create **captions that best reflect Group A** while **being as far removed from Group B as possible**.
- **Write exactly 10 captions**, each reflecting a **distinct and specific concept**.
- Focus on features that are **unique to Group A** and **unlikely to appear in Group B**.
- Do **not** use vague terms like "presence of ..." or "images with ...".
- Do **not** list multiple concepts within parentheses.
- Each caption should reflect only **one distinct visual concept**. Example formats:
    * "a group of people walking through a marketplace"
    * "a round wooden table with decorative plates"
    * "brightly colored flowers in a garden"
    * "a row of parked bicycles along a busy road"
    * "a person wearing a patterned summer outfit"
    * "a backpack filled with books"
  
### Final Output Format:
You must generate exactly **10 distinct hypotheses** that describe differences more likely to be true for Group A compared to Group B.
- Do not leave the list empty.
- If unsure, make reasonable assumptions.
- The output **must** be a list with **10** bullet points.

Please return exactly **10 bullet points** in the following format:
* "..."
* "..."
* "..."

### Step 4: Score and Rank the Hypotheses
Now, for each of the 10 hypotheses above, **evaluate how well it distinguishes Group A from Group B**, using the following scoring system:

- **Score 2**: Strongly describes Group A and is very unlikely for Group B.
- **Score 1**: Describes Group A but might somewhat apply to Group B.
- **Score 0**: Does not clearly distinguish between Group A and Group B.

### Output Format:
Please return the final ranked list in descending order of score:
1. "..." - Score: 2
2. "..." - Score: 2
...
10. "..." - Score: 0

If multiple captions have the same score, rank the more specific or detailed one higher.
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V2 = """
This image contains two groups of images. 20 images from Group A are shown in the first two rows, while 20 images from Group B are shown in the last two rows.

I am a machine learning researcher trying to identify the most significant differences between these two groups.

You will perform a four-step analysis:

---

### Step 1: Identify Key Characteristics
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:
  1. ...
  2. ...
  3. ...
- Group B:
  1. ...
  2. ...
  3. ...

If any image contains **text**, logos, or signs, you **must include those as key features**. You may use OCR or your own capabilities to extract and interpret this information.

---

### Step 2: Compare and Contrast
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- If any image contains text (e.g., packaging labels, product names), you must include and analyze the differences in that text.

#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or functions, not abstract concepts.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include visual details such as material (e.g. satin vs lace), color (white vs pink), or complexity (plain vs decorative).
- If differences are subtle (e.g., chocolate types, printed text), focus on texture, tone, label, or shape.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, natural vs artificial, festive vs neutral, etc.

Please list key differences in each category with at least:
- 2 for Entities
- 3 for Actions
- 3 for Attributes
- 2 for Environments

---

### Step 3: Generate Group A-Focused Hypotheses
Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

! Do NOT write sentences that describe Group B  
! Do NOT mention both A and B in the same sentence  
! Do NOT describe general/shared features

Captions may include textual information seen in the images (e.g., brand names, printed words, product types).

#### Bad vs Good Examples:
- Bad: "Stuffed animals are placed on a shelf" → this is common to both groups  
  Good: "Plush rabbits wearing bow ties arranged in a festive corner display"

- Bad: "Images with text on packaging"  
  Good: "A nutrition label that reads 'High Protein – Vanilla Flavor' on a white bottle"

- Bad: "People standing outdoors"  
  Good: "Two athletes stretching on a running track at sunset"

- Bad: "Colorful items on a table"  
  Good: "Neatly folded silk scarves in floral patterns on a glass display table"

List your 10 captions in the following format:
1. "..."
2. "..."
...

---

### Step 4: Score and Rank the Hypotheses

Evaluate how well each hypothesis distinguishes Group A from Group B:

- **Score 2** = Strong evidence of Group A AND very unlikely to occur in Group B  
- **Score 1** = Reasonable for Group A, but may also appear in Group B  
- **Score 0** = Applies to both groups or is too vague to differentiate

📌 Score based on how strongly the hypothesis favors Group A **AND** rejects Group B.

Then **sort the captions by score in descending order**. If scores are tied, place the more detailed or specific one higher.
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V3 = """
You are given a single image that contains **two groups of images arranged vertically**:

- The **first two rows** (top half) of the image contain 20 images from **Group A**, each marked with a **red border**.
- The **last two rows** (bottom half) of the image contain 20 images from **Group B**, each marked with a **green border**.

I am a machine learning researcher trying to identify the most significant differences between these two groups. Your task is to perform a step-by-step analysis to understand and summarize those differences.

You will perform a four-step analysis:

---

### Step 1: Identify Key Characteristics
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:
  1. ...
  2. ...
  3. ...
- Group B:
  1. ...
  2. ...
  3. ...

If any image contains **text**, logos, or signs, you **must include those as key features**. You may use OCR or your own capabilities to extract and interpret this information.

---

### Step 2: Compare and Contrast
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- If any image contains text (e.g., packaging labels, product names), you must include and analyze the differences in that text.

#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or functions, not abstract concepts.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include visual details such as material (e.g. satin vs lace), color (white vs pink), or complexity (plain vs decorative).
- If differences are subtle (e.g., chocolate types, printed text), focus on texture, tone, label, or shape.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, natural vs artificial, festive vs neutral, etc.

Please list key differences in each category with at least:
- 2 for Entities
- 3 for Actions
- 3 for Attributes
- 2 for Environments

---

### Step 3: Generate Group A-Focused Hypotheses
Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

! Do NOT write sentences that describe Group B  
! Do NOT mention both A and B in the same sentence  
! Do NOT describe general/shared features

Captions may include textual information seen in the images (e.g., brand names, printed words, product types).

#### Bad vs Good Examples:
- Bad: "Stuffed animals are placed on a shelf" → this is common to both groups  
  Good: "Plush rabbits wearing bow ties arranged in a festive corner display"

- Bad: "Images with text on packaging"  
  Good: "A nutrition label that reads 'High Protein – Vanilla Flavor' on a white bottle"

- Bad: "People standing outdoors"  
  Good: "Two athletes stretching on a running track at sunset"

- Bad: "Colorful items on a table"  
  Good: "Neatly folded silk scarves in floral patterns on a glass display table"

List your captions in the following format:
* "..."
* "..."
* "..."
...

---

### Step 4: Score and Rank the Hypotheses

Evaluate how well each hypothesis distinguishes Group A from Group B:

- **Score 2** = Strong evidence of Group A AND very unlikely to occur in Group B  
- **Score 1** = Reasonable for Group A, but may also appear in Group B  
- **Score 0** = Applies to both groups or is too vague to differentiate

Then sort the captions by score in **descending order**. If scores are tied, place the more detailed or specific one higher.

Output only the sorted list of captions in the following format:
1. "..."
2. "..."
3. "..."
...

Do NOT include a score table. Do NOT display any scores.

"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V4 = """
You are an assistant designed for multi-step visual reasoning.  
You must follow a **strict four-step process** to analyze differences between Group A and Group B.

! You are NOT allowed to skip any steps.  
! You MUST output each step, even if the content appears obvious, repetitive, or similar.  
! Your output MUST include clearly marked sections for Step 1, Step 2, Step 3, and Step 4 — in that exact order.

Start your output with:
### Step 1: Identify Key Characteristics


You are given a single image that contains **two groups of images arranged vertically**:

- The **first two rows** (top half) of the image contain 20 images from **Group A**, each marked with a **red border**.
- The **last two rows** (bottom half) of the image contain 20 images from **Group B**, each marked with a **green border**.

I am a machine learning researcher trying to identify the most significant differences between these two groups. Your task is to perform a step-by-step analysis to understand and summarize those differences.

You will perform a four-step analysis:

---

### Step 1: Identify Key Characteristics
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:
  1. ...
  2. ...
  3. ...
- Group B:
  1. ...
  2. ...
  3. ...

If any image contains **text**, logos, or signs, you **must include those as key features**. You may use OCR or your own capabilities to extract and interpret this information.

---

### Step 2: Compare and Contrast
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- If any image contains text (e.g., packaging labels, product names), you must include and analyze the differences in that text.

#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or functions, not abstract concepts.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include visual details such as material (e.g. satin vs lace), color (white vs pink), or complexity (plain vs decorative).
- If differences are subtle (e.g., chocolate types, printed text), focus on texture, tone, label, or shape.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, natural vs artificial, festive vs neutral, etc.

Please list key differences in each category with at least:
- 2 for Entities
- 3 for Actions
- 3 for Attributes
- 2 for Environments

---

### Step 3: Generate Group A-Focused Hypotheses

Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

! Do **NOT** write sentences that describe Group B  
! Do **NOT** mention both A and B in the same sentence  
! Do **NOT** describe general/shared features  
! Do **NOT** write vague captions like "colorful objects" or "animals on a table"

Captions may include textual information seen in the images (e.g., brand names, printed words, product types).

#### Bad vs Good Examples:
- Bad: "Stuffed animals are placed on a shelf" → this is common to both groups  
  Good: "Plush rabbits wearing bow ties arranged in a festive corner display"

- Bad: "Images with text on packaging"  
  Good: "A nutrition label that reads 'High Protein – Vanilla Flavor' on a white bottle"

- Bad: "People standing outdoors"  
  Good: "Two athletes stretching on a running track at sunset"

- Bad: "Colorful items on a table"  
  Good: "Neatly folded silk scarves in floral patterns on a glass display table"

Before finalizing each caption, ask yourself:
- “Is this feature **very likely for Group A**, and **very unlikely for Group B**?”
- If the answer is not a clear **YES**, do not include it.

You **must** format your list using bullet points (`*`), **not** numbers.

Do not write:
1. "..."
2. "..."

Do write:
* "..."
* "..."

---

### Step 4: Score and Rank the Hypotheses

Your task is to score and rank the 10 Group A hypotheses from Step 3.

Each caption must be evaluated for how well it distinguishes Group A from Group B:

- **Score 2** = Strongly unique to Group A, and very unlikely in Group B  
- **Score 1** = Possibly true for Group A, but may also appear in Group B  
- **Score 0** = Too vague or general, likely to apply to both groups

Then, sort the 10 captions by **score in descending order**. If scores are tied, place the more specific or detailed caption higher.

You MUST follow this output rule:
- DO NOT output any scores, score explanations, or tables  
- DO NOT include any heading like "Final Ranking"  
- DO NOT omit the quotation marks  
- DO NOT format using bullet points  
- ONLY output the sorted list using numbered format (1.–10.), and **each caption MUST be wrapped in English double quotes** (")

List the format:
1. "..."
2. "..."
3. "..."
...
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V5 = """
You are an assistant designed for multi-step visual reasoning.  
You must follow a **strict four-step process** to analyze differences between Group A and Group B.

! You are NOT allowed to skip any steps.  
! You MUST output each step, even if the content appears obvious, repetitive, or similar.  
! Your output MUST include clearly marked sections for Step 1, Step 2, Step 3, and Step 4 — in that exact order.

Start your output with:
### Step 1: Identify Key Characteristics

You are given a single image that contains **two groups of images arranged vertically**:

- The **first two rows** (top half) of the image contain 20 images from **Group A**, each marked with a **red border**.
- The **last two rows** (bottom half) of the image contain 20 images from **Group B**, each marked with a **green border**.

I am a machine learning researcher trying to identify the most significant differences between these two groups. Your task is to perform a step-by-step analysis to understand and summarize those differences.

You will perform a four-step analysis:

---

### Step 1: Identify Key Characteristics  
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:  
  1. ...  
  2. ...  
  3. ...  
- Group B:  
  1. ...  
  2. ...  
  3. ...  

If any image contains **text**, logos, or printed signs, you **must extract and include them as key features**.  
You may use OCR or your own capabilities to interpret and transcribe this information, including:
- Brand names  
- Packaging labels  
- Nutrition facts  
- Product descriptions  
- Visible signage or icons

These textual elements are critical and must be included as part of your analysis.

---

### Step 2: Compare and Contrast  
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- If any image contains text (e.g., packaging labels, product names), you must include and analyze the differences in that text.

#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or functions, not abstract concepts.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include visual details such as material (e.g. satin vs lace), color (white vs pink), or complexity (plain vs decorative).
- If differences are subtle (e.g., chocolate types, printed text), focus on texture, tone, label, or shape.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, natural vs artificial, festive vs neutral, etc.

Please list key differences in each category with at least:  
- 2 for Entities  
- 3 for Actions  
- 3 for Attributes  
- 2 for Environments

---

### Step 3: Generate Group A-Focused Hypotheses

Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

! Do **NOT** write sentences that describe Group B  
! Do **NOT** mention both A and B in the same sentence  
! Do **NOT** describe general/shared features  
! Do **NOT** write vague captions like "colorful objects" or "animals on a table"

Captions may include textual information seen in the images (e.g., brand names, printed words, product types).

#### Bad vs Good Examples:  
- Bad: "Stuffed animals are placed on a shelf" → this is common to both groups  
  Good: "Plush rabbits wearing bow ties arranged in a festive corner display"

- Bad: "Images with text on packaging"  
  Good: "A nutrition label that reads 'High Protein – Vanilla Flavor' on a white bottle"

- Bad: "People standing outdoors"  
  Good: "Two athletes stretching on a running track at sunset"

- Bad: "Colorful items on a table"  
  Good: "Neatly folded silk scarves in floral patterns on a glass display table"

Before finalizing each caption, ask yourself:
- “Is this feature **very likely for Group A**, and **very unlikely for Group B**?”
- “Does this caption avoid describing or assuming anything about Group B?”

You **must** format your list using bullet points (`*`), **not** numbers.

Do not write:
1. "..."  
2. "..."

Do write:
* "..."  
* "..."

---

### Step 4: Score and Rank the Hypotheses

Your task is to score and rank the 10 Group A hypotheses from Step 3.

Each caption must be evaluated for how well it distinguishes Group A from Group B:

- **Score 2** = Strongly unique to Group A, and very unlikely in Group B  
- **Score 1** = Possibly true for Group A, but may also appear in Group B  
- **Score 0** = Too vague or general, likely to apply to both groups

Then, sort the 10 captions by **score in descending order**. If scores are tied, place the more specific or detailed caption higher.
If multiple captions have equal score and specificity, prioritize captions that include group-defining textual elements.

You MUST follow this output rule:  
- DO NOT output any scores, score explanations, or tables  
- DO NOT include any heading like "Final Ranking"  
- DO NOT omit the quotation marks  
- DO NOT format using bullet points  
- ONLY output the sorted list using numbered format (1.–10.), and **each caption MUST be wrapped in English double quotes**

List format:
1. "..."  
2. "..."  
3. "..."  
...
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V6 = """"
You are an assistant designed for multi-step visual reasoning.  
You must follow a **strict four-step process** to analyze differences between Group A and Group B.

! You are NOT allowed to skip any steps.  
! You MUST output each step, even if the content appears obvious, repetitive, or similar.  
! Your output MUST include clearly marked sections for Step 1, Step 2, Step 3, and Step 4 — in that exact order.

Start your output with:
### Step 1: Identify Key Characteristics

You are given a single image that contains **two groups of images arranged vertically**:

- The **first two rows** (top half) of the image contain 20 images from **Group A**, each marked with a **red border**.
- The **last two rows** (bottom half) of the image contain 20 images from **Group B**, each marked with a **green border**.

I am a machine learning researcher trying to identify the most significant differences between these two groups. Your task is to perform a step-by-step analysis to understand and summarize those differences.

You will perform a four-step analysis.

Do **not** assume prior knowledge of the group labels or what the groups represent.  
You must discover distinctive features based solely on the content of the images.

---

### Step 1: Identify Key Characteristics  
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:  
  1. ...  
  2. ...  
  3. ...  
- Group B:  
  1. ...  
  2. ...  
  3. ...  

If any image contains **text**, logos, or printed signs, you **must extract and include them as key features**.  
You may use OCR or your own capabilities to interpret and transcribe this information, including:
- Brand names  
- Product descriptions  
- Labels or signs  
- Names of routines, objects, or categories

If certain **textual elements or labels** appear frequently in one group but not the other, treat them as important and mention them explicitly.

---

### Step 2: Compare and Contrast  
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- If any image contains text, phrases, or labels, you must include and compare them.

#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or sequences.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include details such as material, color, design complexity, or structure.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, minimal vs scenic, simple vs decorative, etc.

Please list key differences in each category with at least:  
- 2 for Entities  
- 3 for Actions  
- 3 for Attributes  
- 2 for Environments

---

### Step 2.5: Prioritize Key Semantic Differences

Before generating captions, extract and list the **most semantically distinctive terms or visual features** that are:

- Frequently found in Group A  
- Rare or absent in Group B  
- Strong indicators of group difference  

These may include:
- Repeated text or labels  
- Pose names or flow titles  
- Product categories or brand names  
- Dominant visual materials or structures  
- Packaging types or visual layout

List them as bullet points (not full sentences), sorted by importance.  

Your list must include at least **3 terms that uniquely or predominantly appear in Group A**, not just those that contrast with Group B.
If Group B is strongly associated with one concept, and Group A is visually distinct, you must extract both sides of the contrast.
Do not only focus on Group B-exclusive terms — your goal is to find what makes **Group A visually unique**.


You will use this list to guide Step 3 and Step 4.

---

### Step 3: Generate Group A-Focused Hypotheses

Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

Captions may include textual content observed in the images.

Your 10 captions must follow these content and structure rules:

1. **At least 5 of the captions must directly include terms or features from Step 2.5.**
2. **At least 3 captions must describe structural visual features**, such as diagrams, transitions, or part relationships.
3. **At least 3 captions must describe named flows, object types, or content categories**.
4. Only **one** caption may use a general layout description (e.g., "instructional diagrams").
5. You MUST avoid semantically redundant captions. Each caption must express a unique concept.
6. Do **not** include captions that are semantically redundant. If two captions describe the same core idea using different words, remove one.
7. Do **NOT** write sentences that describe Group B  
8. Do **NOT** mention both A and B in the same sentence  
9. Do **NOT** describe general/shared features  
10. Do **NOT** write vague captions like "colorful objects" or "people doing things"

**When using terms from Step 2.5, you must place the strongest term as the subject or the first phrase of the caption whenever possible.**

Before finalizing each caption, ask yourself:
- “Is this feature **very likely for Group A**, and **very unlikely for Group B**?”
- “Does this caption avoid describing or assuming anything about Group B?”
- “Does this caption mention specific phrases, labels, or concepts that appear only in Group A?”
- “Is the caption focused enough to represent a unique concept, not a general or stylistic impression?”
- “Is this caption meaningfully different from the others I’ve written?”

You **must** format your list using bullet points (`*`), **not** numbers.

Do not write:
1. "..."  
2. "..."

Do write:
* "..."  
* "..."
---

### Step 4: Score and Rank the Hypotheses

Your task is to score and rank the 10 Group A hypotheses from Step 3.

Each caption must be evaluated for how well it distinguishes Group A from Group B:

- **Score 2** = Strongly unique to Group A, and very unlikely in Group B  
- **Score 1** = Possibly true for Group A, but may also appear in Group B  
- **Score 0** = Too vague or general, likely to apply to both groups

Then, sort the 10 captions by **score in descending order**. If scores are tied, place the more specific or detailed caption higher.

Captions that **begin with** a top-ranked term from Step 2.5 must appear at the top of the list, unless they are vague or repetitive.

If a caption includes multiple Step 2.5 terms and starts with one of them, it should be ranked above captions that mention the same terms later or use less distinctive phrasing.

must be placed **higher than captions that describe general layout or design features**.

You MUST follow this output rule:  
- DO NOT output any scores, score explanations, or tables  
- DO NOT include any heading like "Final Ranking"  
- DO NOT omit the quotation marks  
- DO NOT format using bullet points  
- ONLY output the sorted list using numbered format (1.–10.), and **each caption MUST be wrapped in English double quotes**

List format:
1. "..."  
2. "..."  
3. "..."  
...
"""

VLM_PROPOSE_AND_RANK_PROMPT_COT_V7 = """"
You are an assistant designed for multi-step visual reasoning.  
You must follow a **strict four-step process** to analyze differences between Group A and Group B.

! You are NOT allowed to skip any steps.  
! You MUST output each step, even if the content appears obvious, repetitive, or similar.  
! Your output MUST include clearly marked sections for Step 1, Step 2, Step 3, and Step 4 — in that exact order.

Start your output with:
### Step 1: Identify Key Characteristics

You are given a single image that contains **two groups of images arranged vertically**:

- The **first two rows** (top half) of the image contain 20 images from **Group A**, each marked with a **red border**.
- The **last two rows** (bottom half) of the image contain 20 images from **Group B**, each marked with a **green border**.

I am a machine learning researcher trying to identify the most significant differences between these two groups. Your task is to perform a step-by-step analysis to understand and summarize those differences.

You will perform a four-step analysis.

Do **not** assume prior knowledge of the group labels or what the groups represent.  
You must discover distinctive features based solely on the content of the images.

---

### Step 1: Identify Key Characteristics  
Analyze both groups of images and summarize the **most notable characteristics** of Group A and Group B separately. Please list at least **three distinct characteristics** for each group.

- Group A:  
  1. ...  
  2. ...  
  3. ...  
- Group B:  
  1. ...  
  2. ...  
  3. ...  

If any image contains **text**, logos, or printed signs, you **must extract and include them as key features**.  
You may use OCR or your own capabilities to interpret and transcribe this information, including:
- Brand names  
- Product descriptions  
- Labels or signs  
- Names of routines, objects, or categories

If certain **textual elements or labels** appear frequently in one group but not the other, treat them as important and mention them explicitly.

---

### Step 2: Compare and Contrast  
Identify clear and meaningful differences between Group A and Group B. Differences **must belong to one of the following categories**:

#### 1. **Entities (Objects, Animals, People, etc.)**
- The subject may not be a person.
- If Group A and B contain similar entity types, **you must describe their specific features, roles, appearances, or functions to highlight differences**.
- Each characteristic should reflect a **visually distinct trait** that differentiates the groups.
- If any image contains text, phrases, or labels, you must include and compare them.


#### 2. **Actions (What subjects are doing)**
- Focus on visible activities or sequences.

#### 3. **Attributes (Color, Material, Style, Texture, etc.)**
- Include details such as material, color, design complexity, or structure.

#### 4. **Environment (Scene, Background, Setting)**
- Indoor vs outdoor, minimal vs scenic, simple vs decorative, etc.

Please list key differences in each category with at least:  
- 2 for Entities  
- 3 for Actions  
- 3 for Attributes  
- 2 for Environments

---

### Step 2.5: Prioritize Key Semantic Differences

Before generating captions, extract and list the **most semantically distinctive terms or visual features** that are:

- Frequently found in Group A  
- Rare or absent in Group B  
- Strong indicators of group difference  

These may include:
- Repeated text or labels  
- Pose names or flow titles  
- Product categories or brand names  
- Dominant visual materials or structures  
- Packaging types or visual layout

List them as bullet points (not full sentences), sorted by importance.  

Your list must include at least **3 terms that uniquely or predominantly appear in Group A**, not just those that contrast with Group B.
If Group B is strongly associated with one concept, and Group A is visually distinct, you must extract both sides of the contrast.
Do not only focus on Group B-exclusive terms — your goal is to find what makes **Group A visually unique**.


You will use this list to guide Step 3 and Step 4.

---

### Step 3: Generate Group A-Focused Hypotheses

Now, generate **10 distinct and highly specific visual captions** that are:

- Very likely to be **true for Group A**
- Very unlikely to be **true for Group B**
- Focused on **one visual concept per line**

Captions may include textual content observed in the images.

Your 10 captions must follow these content and structure rules:

1. **At least 5 of the captions must directly include terms or features from Step 2.5.**
2. **At least 3 captions must describe structural visual features**, such as diagrams, transitions, or part relationships.
3. **At least 3 captions must describe named flows, object types, or content categories**.
4. Only **one** caption may use a general layout description (e.g., "instructional diagrams").
5. You MUST avoid semantically redundant captions. Each caption must express a unique concept.
6. Do **not** include captions that are semantically redundant. If two captions describe the same core idea using different words, remove one.
7. Do **NOT** write sentences that describe Group B  
8. Do **NOT** mention both A and B in the same sentence  
9. Do **NOT** describe general/shared features  
10. Do **NOT** write vague captions like "colorful objects" or "people doing things"

**When using terms from Step 2.5, you must place the strongest term as the subject or the first phrase of the caption whenever possible.**

Before finalizing each caption, ask yourself:
- “Is this feature **very likely for Group A**, and **very unlikely for Group B**?”
- “Does this caption avoid describing or assuming anything about Group B?”
- “Does this caption mention specific phrases, labels, or concepts that appear only in Group A?”
- “Is the caption focused enough to represent a unique concept, not a general or stylistic impression?”
- “Is this caption meaningfully different from the others I’ve written?”

You **must** format your list using bullet points (`*`), **not** numbers.

Do not write:
1. "..."  
2. "..."

Do write:
* "..."  
* "..."
---

### Step 4: Score and Rank the Hypotheses

Your task is to score and rank the 10 Group A hypotheses from Step 3.

Each caption must be evaluated for how well it distinguishes Group A from Group B:

- **Score 2** = Strongly unique to Group A, and very unlikely in Group B  
- **Score 1** = Possibly true for Group A, but may also appear in Group B  
- **Score 0** = Too vague or general, likely to apply to both groups

Then, sort the 10 captions by **score in descending order**. If scores are tied, place the more specific or detailed caption higher.

Captions that **begin with** a top-ranked term from Step 2.5 must appear at the top of the list, unless they are vague or repetitive.

If a caption includes multiple Step 2.5 terms and starts with one of them, it should be ranked above captions that mention the same terms later or use less distinctive phrasing.

must be placed **higher than captions that describe general layout or design features**.

You MUST follow this output rule:  
- DO NOT output any scores, score explanations, or tables  
- DO NOT include any heading like "Final Ranking"  
- DO NOT omit the quotation marks  
- DO NOT format using bullet points  
- ONLY output the sorted list using numbered format (1.–10.), and **each caption MUST be wrapped in English double quotes**

List format:
1. "..."  
2. "..."  
3. "..."  
...
"""

VLM_PROMPT = """
    This image contains two groups of images. 20 images from Group A are shown in the first two rows, while 20 images from Group B are shown in the last two rows.

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can better understand my data.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*"). For example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not list more than one concept. The hypothesis should be a caption, so hypotheses like "more of ...", "presence of ...", "images with ..." are incorrect. Also do not enumerate possibilities within parentheses. Here are examples of bad outputs and their corrections:
    * INCORRECT: "various nature environments like lakes, forests, and mountains" CORRECTED: "nature"
    * INCORRECT: "images of household object (e.g. bowl, vacuum, lamp)" CORRECTED: "household objects"
    * INCORRECT: "Presence of baby animals" CORRECTED: "baby animals"
    * INCORRECT: "Different types of vehicles including cars, trucks, boats, and RVs" CORRECTED: "vehicles"
    * INCORRECT: "Images involving interaction between humans and animals" CORRECTED: "interaction between humans and animals"
    * INCORRECT: "More realistic images" CORRECTED: "realistic images" 
    * INCORRECT: "Insects (cockroach, dragonfly, grasshopper)" CORRECTED: "insects"

    Please return exactly **10 bullet points**, in the following format:
    * "..."
    * "..."
    * "..."

    Again, I want to figure out what kind of distribution shift are there. List properties that hold more often for the images in group A compared to group B. Answer with a list (separated by bullet points "*"). Your response:
"""

CLIP_FRIENDLY_GROUP_A = """
    The following are the result of captioning a group of images:

    {text}

    I am a machine learning researcher trying to figure out the major commonalities within this group so I can better understand my data.

    Come up with 10 distinct concepts that appear often in the group. Please write a list of captions (separated by bullet points "*") . for example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "caption with one word" and do not list more than one concept. The hypothesis should be a caption, so hypotheses like "presence of ...", "images with ..." are incorrect. Here are examples of bad outputs and their corrections:
    * INCORRECT: "various nature environments like lakes, forests, and mountains" CORRECTED: "nature"
    * INCORRECT: "images of household object (e.g. bowl, vaccuum, lamp)" CORRECTED: "household objects"
    * INCORRECT: "Presence of baby animals" CORRECTED: "baby animals"
    * INCORRECT: "Different types of vehicles including cars, trucks, boats, and RVs" CORRECTED: "vehicles"
    * INCORRECT: "Images involving interaction between humans and animals" CORRECTED: "interaction between humans and animals"

    Again, I want to figure out the common concepts in a group of images. List properties that hold most often for images (not captions) in the group. Answer with a list (separated by bullet points "*"). Your response:
"""

RUIQI_DIFF_PROMPT_MINIMAL_CONTEXT = """
    The following are the result of captioning two groups of images:

    {text}

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can better understand my data.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*") . for example:
    * "a dog next to a horse"
    * "a car in the rain"
    * "low quality"
    * "cars from a side view"
    * "people in a intricate dress"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "captions about bird", or "caption with one word", or "detailed caption". Here are examples of bad outputs and their corrections:
    * bad output: "various nature environments like lakes, forests, and mountains" corrected: "nature environments"
    * bad output: "images of household object (e.g. bowl, vaccuum, lamp)" corrected: "household objects"
    * bad output: "Water-related scenes (ocean, river, catamaran)" corrected: "water" or "water-related"
    * bad output: "Different types of vehicles including cars, trucks, boats, and RVs" corrected: "vehicles"
    * bad output: "Images involving interaction between humans and animals" corrected: "interaction between humans and animals"

    Again, I want to figure out what kind of distribution shift are there. List properties that holds more often for the images in group A compared to group B. Your response:
"""

DIFFUSION_LLM_PROMPT = """
    The following are the result of captioning two groups of images generated by two different image generation models, with each pair of captions corresponding to the same generation prompt:

    {text}

    I am a machine learning researcher trying to figure out the major differences between these two groups so I can correctly identify which model generated which image for unseen prompts.

    Come up with 10 distinct concepts that are more likely to be true for Group A compared to Group B. Please write a list of captions (separated by bullet points "*") . for example:
    * "dogs with brown hair"
    * "a cluttered scene"
    * "low quality"
    * "a joyful atmosphere"

    Do not talk about the caption, e.g., "caption with one word" and do not list more than one concept. The hypothesis should be a caption that can be fed into CLIP, so hypotheses like "more of ...", "presence of ...", "images with ..." are incorrect. Also do not enumerate possibiliites within parentheses. Here are examples of bad outputs and their corrections:
    * INCORRECT: "various nature environments like lakes, forests, and mountains" CORRECTED: "nature"
    * INCORRECT: "images of household object (e.g. bowl, vaccuum, lamp)" CORRECTED: "household objects"
    * INCORRECT: "Presence of baby animals" CORRECTED: "baby animals"
    * INCORRECT: "Images involving interaction between humans and animals" CORRECTED: "interaction between humans and animals"
    * INCORRECT: "More realistic images" CORRECTED: "realistic images" 
    * INCORRECT: "Insects (cockroach, dragonfly, grasshopper)" CORRECTED: "insects"

    Again, I want to figure out what the main differences are between these two image generation models so I can correctly identify which model generated which image. List properties that hold more often for the images (not captions) in group A compared to group B. Answer with a list (separated by bullet points "*"). Your response:
"""
