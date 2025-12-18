// app/components/VenueCard.tsx
import Image from 'next/image'

interface EntityConfig {
  summaryField: string
  cardFields: Array<{ field: string; suffix?: string }>
}

interface VenueCardProps {
  listing: any
  entityConfig: EntityConfig
}

export default function VenueCard({ listing, entityConfig }: VenueCardProps) {
  return (
    <a
      href={`/listing/${listing.slug}`}
      className="bg-card text-card-foreground rounded-lg shadow-md hover:shadow-xl transition-shadow overflow-hidden"
    >
      <div className="h-48 bg-linear-to-br from-primary/20 to-primary/30 flex items-center justify-center">
        <span className="text-primary text-6xl font-bold">
          {listing.entity_name.charAt(0).toUpperCase()}
        </span>
      </div>

      <div className="p-6">
        <h3 className="text-xl font-bold mb-2">
          {listing.entity_name}
        </h3>

        <p className="text-sm text-muted-foreground mb-3">
          {listing.city} • {listing.postcode}
        </p>

        {/* Category-specific summary */}
        {listing.venues && (() => {
          const summary = listing.venues[entityConfig.summaryField]
          
          if (summary && typeof summary === 'string') {
            return (
              <p className="text-sm text-card-foreground mb-3 line-clamp-5">
                {summary}
              </p>
            )
          }
          return null
        })()}

        <div className="flex gap-2 flex-wrap">
          {/* Category-specific fields */}
          {listing.venues && entityConfig.cardFields.map(({ field, suffix }) => {
            const value = listing.venues[field]
            
            if (value !== null && value !== undefined) {
              return (
                <span 
                  key={field}
                  className="px-3 py-1 rounded-full text-xs bg-primary/20 text-primary font-medium"
                >
                  {value} {suffix || ''}
                </span>
              )
            }
            return null
          })}
          
          <span className="px-3 py-1 rounded-full text-xs bg-muted text-muted-foreground capitalize font-medium">
            venue
          </span>
        </div>
      </div>
    </a>
  )
}