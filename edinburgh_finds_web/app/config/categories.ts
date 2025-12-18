// app/config/categories.ts

export const categories: Record<string, CategoryConfig> = {
  padel: {
    name: "Padel",
    image: "/images/categories/padel.jpg",
    isLive: true,
    
    venue: {
      summaryField: 'padel_summary',
      cardFields: [
        { field: 'padel_total_courts', suffix: 'courts' }
      ]
    }
    // Add retailer, coach, club configs later
  },
  
  tennis: {
    name: "Tennis",
    image: "/images/categories/tennis.jpg",
    isLive: true,
    
    venue: {
      summaryField: 'tennis_summary',
      cardFields: [
        { field: 'tennis_total_courts', suffix: 'courts' }
      ]
    }
  },
  
  pickleball: {
    name: "Pickleball",
    image: "/images/categories/pickleball.jpg",
    isLive: false,
    
    venue: {
      summaryField: 'pickleball_summary',
      cardFields: [
        { field: 'pickleball_total_courts', suffix: 'courts' }
      ]
    }
  },

  'board-games': {
    name: "Board Games",
    image: "/images/categories/board-games.jpg",
    isLive: false,
    
    venue: {
      summaryField: 'board_games_summary',
      cardFields: []
    }
  },

  football: {
    name: "Football",
    image: "/images/categories/football.jpg",
    isLive: false,
    
    venue: {
      summaryField: 'football_summary',
      cardFields: [
        { field: 'football_total_pitches', suffix: 'pitches' }
      ]
    }
  },

  pilates: {
    name: "Pilates",
    image: "/images/categories/pilates.jpg",
    isLive: false,
    
    venue: {
      summaryField: 'pilates_summary',
      cardFields: [
        { field: 'pilates_total_studios', suffix: 'studios' }
      ]
    }
  }
}

// TypeScript type
export type EntityConfig = {
  summaryField: string
  cardFields: Array<{ field: string; suffix?: string }>
}

export type CategoryConfig = {
  name: string
  image: string
  isLive: boolean
  venue?: EntityConfig
  retailer?: EntityConfig
  coach?: EntityConfig
  club?: EntityConfig
  event?: EntityConfig
}