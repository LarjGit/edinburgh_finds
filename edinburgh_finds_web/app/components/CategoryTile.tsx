import Image from 'next/image'
import Link from 'next/link'

interface CategoryTileProps {
  slug: string;
  name: string;
  image: string;
  isLive: boolean;
}

export default function CategoryTile({ slug, name, image, isLive }: CategoryTileProps) {
  // If coming soon, show non-clickable tile
  if (!isLive) {
    return (
        <div className="relative group overflow-hidden rounded-lg shadow-lg">
        {/* Image */}
        <div className="relative h-64 w-full bg-black">
            <Image
              src={image}
              alt={name}
              fill
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              className="object-cover opacity-40"
            />
            
            {/* Category Name - Bottom Left (like live tiles) */}
            <div className="absolute bottom-0 left-0 right-0 p-6">
            <h3 className="text-2xl font-bold text-white">{name}</h3>
            </div>
            
            {/* Coming Soon Badge - Centered */}
            <div className="absolute inset-0 flex items-center justify-center">
            <span className="inline-block bg-primary text-primary-foreground px-4 py-2 rounded-full text-sm font-semibold">
                Coming Soon
            </span>
            </div>
        </div>
        </div>
    )
    }
  // Live category - clickable
  return (
    <Link href={`/category/${slug}`} className="relative group overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition-shadow">
      {/* Image */}
      <div className="relative h-64 w-full">
        <Image
          src={image}
          alt={name}
          fill
          className="object-cover group-hover:scale-105 transition-transform duration-300"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        {/* Dark gradient overlay for text readability */}
        <div className="absolute inset-0 bg-linear-to-t from-black/70 to-transparent" />
        
        {/* Category Name */}
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <h3 className="text-2xl font-bold text-white">{name}</h3>
        </div>
      </div>
    </Link>
  )
}