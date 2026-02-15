// API Response Types

export interface HealthResponse {
  status: string
  version: string
  features: {
    anti_gaming: string
    rate_limiting: string
  }
  database: {
    status: string
    stats: {
      agents_count: number
      songs_count: number
      tools_count: number
      votes_count: number
    }
  }
  redis: string
}

export interface Song {
  id: string
  title: string
  artist: string
  platform: string
  platform_url?: string
  genre?: string
  mood?: string
  tempo?: number
  up_votes: number
  down_votes: number
  score: number
  weighted_score?: number
  total_votes: number
  rank: number
  created_at: string
}

export interface Tool {
  id: string
  name: string
  website: string
  affiliate_link?: string
  category: string
  features?: string
  pricing?: string
  up_votes: number
  down_votes: number
  score: number
  weighted_score?: number
  total_votes: number
  rank: number
  rating?: number
  review_count?: number
  created_at: string
}

export interface VoteRequest {
  agent_id?: string
  item_type: 'song' | 'tool'
  item_id: string
  vote: 1 | -1
  comment?: string
}

export interface VoteResponse {
  success: boolean
  message: string
  vote?: {
    id: string
    item_type: string
    item_id: string
    vote: number
  }
}

export interface TrendingItem {
  songs: Song[]
  tools: Tool[]
  updated_at: string
}

export interface Top50Item {
  period: string
  items: Array<{
    id: string
    item_type: 'song' | 'tool'
    title?: string
    name?: string
    artist?: string
    platform?: string
    category?: string
    website?: string
    score: number
    total_votes: number
    rank: number
  }>
  total_count: number
  updated_at: string
}
