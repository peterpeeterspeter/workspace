export interface Match {
  id: string
  homeTeam: string
  awayTeam: string
  date: Date
  status: 'scheduled' | 'live' | 'finished'
  homeScore?: number
  awayScore?: number
  prediction?: Prediction
}

export interface Prediction {
  homeWin: number
  draw: number
  awayWin: number
  confidence: number
  recommended: 'home' | 'draw' | 'away'
  valueBet: boolean
  reasoning: string
}

export interface Team {
  id: string
  name: string
  slug: string
  position: number
  points: number
  played: number
  won: number
  drawn: number
  lost: number
  goalsFor: number
  goalsAgainst: number
}
