import { getArticleById, getAllArticles } from "@/lib/articles"
import { Header } from "@/components/header"
import { notFound } from "next/navigation"
import Image from "next/image"

export async function generateStaticParams() {
  const articles = getAllArticles()
  return articles.map((article) => ({
    id: article.id,
  }))
}

export default async function ArticlePage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const article = getArticleById(id)

  if (!article) {
    notFound()
  }

  return (
    <>
      <Header />
      <main style={{ maxWidth: "700px", margin: "40px auto", padding: "0 20px" }}>
        <article>
          <p
            style={{
              fontFamily: "var(--font-sans)",
              fontSize: "0.85rem",
              color: "#999",
              marginBottom: "10px",
            }}
          >
            {article.category} • {article.date}
          </p>
          <h1
            style={{
              fontSize: "2.5rem",
              marginBottom: "30px",
              color: "#5C554F",
              lineHeight: "1.2",
            }}
          >
            {article.title}
          </h1>
          <div style={{ marginBottom: "40px", overflow: "hidden", maxHeight: "350px" }}>
            <Image
              src={`/images/${article.image}`}
              alt={article.title}
              width={700}
              height={350}
              style={{ width: "100%", height: "auto", display: "block", objectFit: "cover" }}
            />
          </div>
          {article.content.map((paragraph, index) => (
            <p
              key={index}
              style={{
                fontSize: "1.1rem",
                lineHeight: "1.8",
                marginBottom: "20px",
                color: "#403D39",
              }}
              dangerouslySetInnerHTML={{ __html: paragraph }}
            />
          ))}
        </article>
      </main>
    </>
  )
}
