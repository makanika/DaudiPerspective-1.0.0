export interface Article {
  id: string
  title: string
  category: string
  date: string
  image: string
  content: string[]
}

import articlesData from "@/data/articles.json"

export function getAllArticles(): Article[] {
  return articlesData.articles
}

export function getArticleById(id: string): Article | undefined {
  return articlesData.articles.find((article) => article.id === id)
}

export function getArticlesByCategory(category: string): Article[] {
  return articlesData.articles.filter((article) => article.category === category)
}
