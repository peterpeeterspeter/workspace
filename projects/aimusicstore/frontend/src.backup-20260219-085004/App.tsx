import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import TrendingPage from './pages/TrendingPage'
import Top50Page from './pages/Top50Page'
import SongDetailPage from './pages/SongDetailPage'
import ToolDetailPage from './pages/ToolDetailPage'
import ComingSoonPage from './pages/ComingSoonPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/trending" element={<TrendingPage />} />
        <Route path="/top" element={<Top50Page />} />
        <Route path="/songs/:id" element={<SongDetailPage />} />
        <Route path="/tools/:id" element={<ToolDetailPage />} />
        <Route path="/waitlist" element={<ComingSoonPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
