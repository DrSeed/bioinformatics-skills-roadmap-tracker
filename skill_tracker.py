# Score bioinformatics competencies and rank the biggest weighted skill gaps.
import csv
import os

COMPETENCIES = [
    "programming",
    "statistics",
    "genomics",
    "data_wrangling",
    "visualisation",
    "communication",
    "reproducibility",
]

# Your honest current level, 0-10.
current = {
    "programming": 6,
    "statistics": 4,
    "genomics": 7,
    "data_wrangling": 6,
    "visualisation": 5,
    "communication": 3,
    "reproducibility": 4,
}

# Where you want to be for your target role, 0-10.
target = {
    "programming": 8,
    "statistics": 8,
    "genomics": 8,
    "data_wrangling": 7,
    "visualisation": 7,
    "communication": 8,
    "reproducibility": 8,
}

# How much the target role depends on each skill, 0-1.
importance = {
    "programming": 0.8,
    "statistics": 0.9,
    "genomics": 0.7,
    "data_wrangling": 0.6,
    "visualisation": 0.6,
    "communication": 0.9,
    "reproducibility": 0.8,
}


def priority_scores(current, target, importance):
    # Weighted positive gap per competency.
    scores = {}
    for c in COMPETENCIES:
        gap = max(target[c] - current[c], 0)
        scores[c] = gap * importance[c]
    return scores


def main():
    scores = priority_scores(current, target, importance)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

    os.makedirs("results", exist_ok=True)
    out_path = os.path.join("results", "priorities.csv")
    with open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["competency", "current", "target", "importance", "priority"])
        for c, s in ranked:
            writer.writerow([c, current[c], target[c], importance[c], round(s, 3)])

    print("Priority order (work on the top ones first):")
    for c, s in ranked:
        print("  {0:15s} priority {1:.2f}".format(c, s))
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
