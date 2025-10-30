import Link from "next/link"

export function Header() {
  return (
    <header
      style={{
        backgroundColor: "#FDFDFB",
        borderBottom: "1px solid #E8E8E8",
        padding: "20px 0",
      }}
    >
      <div style={{ maxWidth: "900px", margin: "0 auto", padding: "0 20px" }}>
        <h1
          style={{
            fontFamily: "var(--font-sans)",
            fontSize: "2rem",
            marginBottom: "10px",
            color: "#5C554F",
          }}
        >
          <Link href="/">Daudi&apos;s Perspective</Link>
        </h1>
        <nav
          style={{
            fontFamily: "var(--font-sans)",
            fontSize: "0.9rem",
          }}
        >
          <Link href="/" style={{ marginRight: "20px", color: "#5C554F" }}>
            All
          </Link>
          <Link href="/category/automotive" style={{ marginRight: "20px", color: "#5C554F" }}>
            Automotive
          </Link>
          <Link href="/category/networks" style={{ marginRight: "20px", color: "#5C554F" }}>
            Networks
          </Link>
          <Link href="/category/aviation" style={{ marginRight: "20px", color: "#5C554F" }}>
            Aviation
          </Link>
          <Link href="/category/linux" style={{ marginRight: "20px", color: "#5C554F" }}>
            Linux
          </Link>
          <Link href="/category/python" style={{ marginRight: "20px", color: "#5C554F" }}>
            Python
          </Link>
          <Link href="/category/embedded" style={{ color: "#5C554F" }}>
            Embedded
          </Link>
        </nav>
      </div>
    </header>
  )
}
