```{mermaid}
classDiagram

class text {
    <<conversation>>
    text_id("Text ID")
}

class u {
    <<utterance>>
    n("Consecutive utterance number")
    who("Speaker ID")
    trans("Transition type")
    whoConfidence("Attribution confidence")
}

class w {
    <<token>>
    pos("part-of-speech tag [CLAWS]")
    lemma("lemmatised form")
    class("“simple” POS tag or major word-class")
    usas("semantic tag [USAS]")
}

class meta_speaker {
    <<meta_speaker>>
    id("Speaker ID")
    exactage("Exact age")
    age1994("Age (BNC1994 groups)")
    agerange("Age range")
    gender("Gender")
    nat("Nationality")
    birthplace("Place of birth")
    birthcountry("Country of birth")
    l1("First language")
    lingorig("Linguistic origin")
    dialect_rep("Accent/dialect as reported")
    hab_city("City/town living")
    hab_country("Country living")
    hab_dur("Duration living (years)")
    dialect_l1("Dialect at Level 1")
    dialect_l2("Dialect at Level 2")
    dialect_l3("Dialect at Level 3")
    dialect_l4("Dialect at Level 4")
    edqual("Highest qualification")
    occupation("Occupation: title")
    socgrade("Class: Social grade")
    nssec("Class: NS-SEC")
    l2("L2 (if bilingual)")
    fls("Foreign languages spoken")
    in_core("Part of core set of speakers")
}

class meta_text {
    <<meta_text>>
    text_id("Text ID")
    rec_length("Recording length")
    rec_date("Recording date")
    rec_year("Year of recording")
    rec_period("Recording period")
    n_speakers("Number of speakers")
    list_speakers("List of speaker IDs")
    rec_loc("Recording location")
    relationships("Inter-speaker relationship")
    topics("Topics covered")
    activity("Activity description")
    conv_type("Selected characterisations of conversation type")
    conventions("Transcription conventions used")
    in_sample("Sample release inclusion")
    transcriber("Transcriber")
}

text ..* u : contains
u ..* w : contains
text .. meta_text : text_id
u .. meta_speaker : who=id
```
