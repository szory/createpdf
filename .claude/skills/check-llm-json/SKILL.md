---
name: check-llm-json
description: Run create_json/llmjsonpdf.py and verify that the JSON the LLM generates from the query in `create_json/query_json.txt` is correct and matches the DataProtocol model. Use when asked to "check the generated json", "check query output" or after changing the prompt template.
---

# Check JSON generated from `query_json.txt` (llmjsonpdf.py)

Goal: verify the JSON produced by `json_details_of_offer(query)` in `create_json/llmjsonpdf.py` against (a) the content of `create_json/query_json.txt` (loaded by `__main__` as `query`) and (b) the structure expected by `DataProtocol` in `models/dataProtocol.py`. Focus on the generated data, not on the logic of the other `*.py` files.

## Steps

1. Read `create_json/llmjsonpdf.py` (prompt template + loading of `query_json.txt` in `__main__`), `create_json/query_json.txt` (the query text) and `models/dataProtocol.py` (expected fields).
2. Run the script, saving output to the scratchpad so the console encoding does not hide Polish characters:
   `cd create_json && PYTHONIOENCODING=utf-8 python llmjsonpdf.py > <scratchpad>/out.txt`
   (needs Ollama running at `http://localhost:11434`; the call can take a while, use a long timeout.)
3. Read `<scratchpad>/out.txt` with the Read tool (not via console `print`: Windows consoles show `ń`, `ż` as `�` even when the data is fine).
4. Compare the JSON with the content of `query_json.txt`, field by field:
   - header: `data`, `adres`, `miejsce_badan`
   - `petla_zwarcia`: entry count per location, `pomiar` values, `nr` running 1..N, defaults (`B`, 16, 230)
   - `rcd`: count, `producent`, `typ`, `amper_rcd` (digits before `/` in `typ`), `amper_wywolania` (default 30), `amper_wywolania_pomiar`, `czas_pomiar`, `usterki` ("brak")
   - `rezystancjaIzolacjiMieszkania`: counts of each cable type, `ileFaz`, string `nr`
   - `rezystancjaIzolacji` is `[]`; `uklad_zasilania`; `napiecie_sieci_zasilajacej`
5. Check structure: valid JSON, top-level `ileFaz`, cables grouped under `przewody` with `_mm2` key spelling (`YKY_5x10_mm2`, `YDYp_3x2_5_mm2`, `YDYp_3x1_5_mm2`, `YDYp_5x2_5_mm2`), `nr` as strings.
6. Validate by loading: `DataProtocol(**json.loads(text))` (run with `sys.path` containing the project root).
7. Report: what matches, what is wrong (with field names), and whether a prompt-template change is needed. Do not edit code unless asked.
8. Copy out.text file into `create_json` folder after  pipeline

## Known pitfalls
- The prompt must ask for `usterki` in every `rcd` entry, otherwise `Rcd(**...)` raises `TypeError`.
- Output may be wrapped in a code fence; `json_details_of_offer` strips it.
- To check a different query, edit `create_json/query_json.txt` (not the Python file).
- Typos in the query (missing commas) are harmless to the LLM but note them if they affect the data.
