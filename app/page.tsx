import { getAllArticles } from "@/lib/articles"
import { Header } from "@/components/header"
import Link from "next/link"
import Image from "next/image"

export default function HomePage() {
  const articles = getAllArticles()

  return (
    <>
      <Header />
      <main style={{ maxWidth: "900px", margin: "40px auto", padding: "0 20px" }}>
        {articles.map((article, index) => (
          <article key={article.id} style={{ marginBottom: "60px" }}>
            <div
              style={{
                fontFamily: "var(--font-sans)",
                fontSize: "0.9rem",
                color: "#8B8680",
                marginBottom: "1rem",
              }}
            >
              {article.date} • {article.category}
            </div>

            <Link href={`/article/${article.id}`}>
              <div
                style={{
                  marginBottom: "1.5rem",
                  overflow: "hidden",
                  borderRadius: "8px",
                  height: "300px",
                }}
              >
                <Image
                  src={`/images/${article.image}`}
                  alt={article.title}
                  width={900}
                  height={300}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                  }}
                />
              </div>
            </Link>

            <h2
              style={{
                fontSize: "1.5rem",
                marginBottom: "1rem",
                color: "#5C554F",
                fontWeight: "700",
              }}
            >
              <Link href={`/article/${article.id}`} style={{ color: "inherit", textDecoration: "none" }}>
                {article.title}
              </Link>
            </h2>

            <p
              style={{
                fontSize: "1.125rem",
                lineHeight: "1.8",
                color: "#403D39",
                marginBottom: "1rem",
              }}
            >
              {article.content[0]}
            </p>

            <Link
              href={`/article/${article.id}`}
              style={{
                fontSize: "0.875rem",
                fontWeight: "600",
                color: "#5C554F",
                textDecoration: "none",
                display: "inline-block",
              }}
            >
              Read More →
            </Link>

            {index < articles.length - 1 && (
              <hr
                style={{
                  border: "0",
                  height: "1px",
                  backgroundImage:
                    "linear-gradient(to right, rgba(0, 0, 0, 0), rgba(64, 61, 57, 0.2), rgba(0, 0, 0, 0))",
                  marginTop: "3rem",
                  marginBottom: "3rem",
                }}
              />
            )}
          </article>
        ))}
      </main>
    </>
  )
}
