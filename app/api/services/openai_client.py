from openai import OpenAI
from .openai_prompt import SCHEMA, SYSTEM_PROMPT
from typing import Dict, Any
import os, json, re
from dotenv import load_dotenv

load_dotenv()

class TextAnalyzer:
    def __init__(self, model: str = "gpt-4.1", temperature: float = 0.1):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.system_prompt = SYSTEM_PROMPT

    def analyze(self, user_text: str) -> Dict[str, Any]:
        user_text = user_text.strip('"').strip("'")
        response = self.client.chat.completions.create(
            model=self.model,
            seed=3,
            temperature=self.temperature,
            response_format={"type": "json_schema", "json_schema": SCHEMA},
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_text},
            ],
        )
        analysis_content = response.choices[0].message.content
        result = json.loads(analysis_content)
        return self._postprocess_scores(user_text=user_text, result=result)

    # ---------- Pós-processamento ----------
    def _postprocess_scores(self, user_text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        criterios = result.get("criterios", {})

        def round_down_40(n: int) -> int:
            n = max(0, min(200, int(n)))
            return (n // 40) * 40

        for k in ["coerencia", "coesao", "norma", "repertorio", "intervencao"]:
            if k in criterios and isinstance(criterios[k], dict):
                if "nota" in criterios[k]:
                    criterios[k]["nota"] = round_down_40(criterios[k]["nota"])

        rep_level = self._detect_repertorio_level(user_text)
        if "repertorio" in criterios:
            nota_c2 = criterios["repertorio"].get("nota", 0)
            if rep_level == "none":
                nota_c2 = min(nota_c2, 80)
            elif rep_level == "weak":
                nota_c2 = min(nota_c2, 120)
            criterios["repertorio"]["nota"] = round_down_40(nota_c2)

        c5_count = self._count_intervention_elements(user_text)
        if "intervencao" in criterios:
            nota_c5 = criterios["intervencao"].get("nota", 0)
            if c5_count <= 3:
                nota_c5 = min(nota_c5, 80)
            elif c5_count == 4:
                nota_c5 = min(nota_c5, 120)
            criterios["intervencao"]["nota"] = round_down_40(nota_c5)

        for k in ["coerencia", "coesao", "norma", "repertorio", "intervencao"]:
            if k in criterios and isinstance(criterios[k], dict):
                nota = criterios[k].get("nota", 0)
                criterios[k]["stars"] = max(0, min(5, nota // 40))

        result["nota_total"] = sum(
            criterios[c].get("nota", 0)
            for c in ["coerencia", "coesao", "norma", "repertorio", "intervencao"]
        )
        result["criterios"] = criterios
        return result

    def _detect_repertorio_level(self, text: str) -> str:
        t = text.lower()
        cues = [
            r"\b\d{4}\b",
            r"\b(\d+\s?%)\b",
            r"\bsegundo\b|\bde acordo com\b|\bdados\b|\bpesquisa\b|\bestudo\b",
            r"\bibge\b|\bonu\b|\boms\b|\bunesco\b|\bstf\b|\bconstituiç[aã]o\b",
            r"\blei\s+\d+|\bart(\.|igo)\s+\d+|\bec\s*\d+",
            r"\bpl\s*\d+|\bpec\s*\d+",
            r"\b(arist[oó]teles|durkheim|foucault|bourdieu|kant|hobbes|locke|rousseau)\b",
        ]
        hits = sum(1 for pat in cues if re.search(pat, t))
        if hits == 0: return "none"
        if hits == 1: return "weak"
        return "strong"

    def _count_intervention_elements(self, text: str) -> int:
        t = text.lower()
        count = 0
        if re.search(r"\b(governo|estado|prefeitura|minist[eé]rio|escolas?|bancos?|institui[cç][aã]o|m[ií]dia|sociedade|ongs?)\b", t):
            count += 1
        if re.search(r"\b(deve(m)?|precisa(m)?|[ée] necessário|implementar|promover|investir|criar|ampliar)\b", t):
            count += 1
        if re.search(r"\bpor meio de|atrav[eé]s de|via|mediante|com\b", t):
            count += 1
        if re.search(r"\ba fim de|para que|de modo a|com o objetivo de|visando\b", t):
            count += 1
        if re.search(r"\bperiodicamente|semanal|mensal|nacional|campanhas?|programas?|plataforma|aplicativo|curr[ií]culo|hor[aá]rio|orçamento|parceria\b", t):
            count += 1
        return count
