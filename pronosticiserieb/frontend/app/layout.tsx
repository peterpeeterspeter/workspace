import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Pronostici Serie B | Previsioni Calcio & Scommesse',
  description: 'Pronostici gratuiti per la Serie B. Analisi AI, statistiche detailed, consigli scommesse. Previsioni accurate per ogni giornata.',
  keywords: ['pronostici serie b', 'scommesse serie b', 'schedine serie b', 'consigli calcio'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="it">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
          <Header />
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  )
}

function Header() {
  return (
    <header className="bg-gray-950 border-b border-gray-800">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-3xl">⚽</div>
          <div>
            <h1 className="text-2xl font-bold text-white">Pronostici Serie B</h1>
            <p className="text-sm text-gray-400">AI-Powered Football Predictions</p>
          </div>
        </div>
        <nav className="hidden md:flex gap-6">
          <a href="/" className="text-gray-300 hover:text-white transition">Home</a>
          <a href="/pronostici" className="text-gray-300 hover:text-white transition">Pronostici</a>
          <a href="/classifica" className="text-gray-300 hover:text-white transition">Classifica</a>
          <a href="/squadre" className="text-gray-300 hover:text-white transition">Squadre</a>
          <a href="/guide" className="text-gray-300 hover:text-white transition">Guide Scommesse</a>
        </nav>
      </div>
    </header>
  )
}

function Footer() {
  return (
    <footer className="bg-gray-950 border-t border-gray-800 mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-white font-bold mb-4">Pronostici Serie B</h3>
            <p className="text-gray-400 text-sm">
              Previsioni AI per la Serie B italiana. Analisi statistiche avanzate e consigli scommesse gratuiti.
            </p>
          </div>
          <div>
            <h3 className="text-white font-bold mb-4">Link Rapidi</h3>
            <ul className="space-y-2 text-sm">
              <li><a href="/pronostici" className="text-gray-400 hover:text-white">Pronostici Oggi</a></li>
              <li><a href="/classifica" className="text-gray-400 hover:text-white">Classifica Serie B</a></li>
              <li><a href="/squadre" className="text-gray-400 hover:text-white">Tutte le Squadre</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-white font-bold mb-4">Legale</h3>
            <p className="text-gray-400 text-sm">
              Gioca responsabilmente. Il gioco può causare dipendenza patologica. 18+
            </p>
            <p className="text-gray-500 text-xs mt-2">
              © 2025 PronosticiSerieB. Tutti i diritti riservati.
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
