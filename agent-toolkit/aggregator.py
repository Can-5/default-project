#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aggregator — Ajans sonuçlarını tek raporda birleştiren."""


class Aggregator:
    def __init__(self, results):
        self.results = results

    def severity_counts(self):
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for res in self.results.values():
            for f in res.get("findings", []):
                sev = f.get("severity", "low")
                counts[sev] = counts.get(sev, 0) + 1
        return counts

    def build_report(self):
        total_findings = sum(len(r.get("findings", [])) for r in self.results.values())
        counts = self.severity_counts()
        agents = list(self.results.keys())

        lines = []
        lines.append("==============================================")
        lines.append("  AGENT-TOOLKIT AGREGADE RAPORU")
        lines.append("==============================================")
        lines.append(f"Katılımcı ajanlar: {', '.join(agents)}")
        lines.append(f"Toplam bulgu: {total_findings}")
        lines.append(f"  Kritik: {counts['critical']} | Yüksek: {counts['high']} | Orta: {counts['medium']} | Düşük: {counts['low']}")
        lines.append("----------------------------------------------")
        for name, res in self.results.items():
            lines.append(f"[{name}] dosya: {res['files_scanned']}, bulgu: {len(res['findings'])}")
        lines.append("==============================================")
        return "\n".join(lines)

    def to_json(self):
        import json
        return json.dumps({
            "agents": list(self.results.keys()),
            "total_findings": sum(len(r.get("findings", [])) for r in self.results.values()),
            "severity_counts": self.severity_counts(),
            "results": self.results,
        }, ensure_ascii=False, indent=2)