import pandas as pd

CSV_PATH = "data/articles.csv"

df = pd.read_csv(CSV_PATH)

# 현재 CSV가 이미 망가져서 image_url 칼럼은 있는데 값이 날짜처럼 들어간 경우 복구
if "image_url" in df.columns:
    # image_url 칼럼에 날짜가 들어간 경우 = 한 칸씩 밀린 상태
    first_image_value = str(df.loc[0, "image_url"])

    if first_image_value.startswith("20"):
        print("감지: image_url 칼럼에 날짜가 들어가 있어 컬럼 밀림을 복구합니다.")

        df["category"] = df["summary_ko"]
        df["summary_ko"] = df["summary"]
        df["summary"] = df["published_at"]
        df["published_at"] = df["image_url"]
        df["image_url"] = ""
else:
    print("감지: image_url 칼럼이 없어 새로 추가합니다.")
    df.insert(4, "image_url", "")

# franchise 칼럼이 없으면 추가
if "franchise" not in df.columns:
    df["franchise"] = "Star Wars"

# 최종 컬럼 순서 고정
df = df[
    [
        "title",
        "title_ko",
        "source_name",
        "source_url",
        "image_url",
        "published_at",
        "summary",
        "summary_ko",
        "category",
        "franchise",
    ]
]

df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")

print("복구 완료: data/articles.csv")
print(df.columns.tolist())
print(df.loc[0, ["source_url", "image_url", "published_at", "summary", "summary_ko", "category", "franchise"]])