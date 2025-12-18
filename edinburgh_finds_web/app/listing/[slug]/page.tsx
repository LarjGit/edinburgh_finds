// app/listing/[slug]/page.tsx
import { prisma } from '@/lib/prisma'
import { notFound } from 'next/navigation'
import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'
import { categories } from '@/app/config/categories'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { FaFacebookF, FaInstagram, FaXTwitter } from 'react-icons/fa6'
import Image from 'next/image'

export default async function ListingPage({ 
  params 
}: { 
  params: Promise<{ slug: string }> 
}) {
  const { slug } = await params
  
  const listing = await prisma.listings.findUnique({
    where: { slug: slug },
    include: { venues: true }
  })

  if (!listing) {
    notFound()
  }

  return (
    <>
      <Navigation />
      
      {/* Hero Section - Split Layout */}
      <section className="relative h-64 md:h-80 bg-linear-to-br from-primary to-primary/80">
        <div className="container mx-auto h-full flex">
          
          {/* Left side - Text/Info */}
          <div className="relative z-10 flex-1 flex flex-col justify-between px-4 py-6">
            {/* Breadcrumb */}
            <div className="text-sm text-white/90">
              <a href="/" className="hover:text-white transition-colors">Home</a>
              <span className="mx-2">›</span>
              <span className="text-white capitalize">{listing.entity_type}s</span>
              <span className="mx-2">›</span>
              <span className="text-white">{listing.entity_name}</span>
            </div>

            {/* Venue Name */}
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
                {listing.entity_name}
              </h1>
              {listing.city && (
                <span className="text-white/90 text-lg flex items-center gap-1">
                  📍 {listing.city}, {listing.postcode}
                </span>
              )}
            </div>
          </div>

          {/* Right side - Photo (hidden on mobile, shown on desktop) */}
          <div className="hidden md:block relative w-[42%] h-full overflow-hidden">
            <Image
              src={`/images/venues/${listing.slug}/hero.jpg`}
              alt={`${listing.entity_name} exterior view`}
              fill
              className="object-cover"
              priority
            />
          </div>
        </div>
      </section>
      
      {/* Main Content */}
      <section className="bg-secondary py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            
            {/* Quick Facts Bar */}
            {listing.venues && (
              <Card className="mb-4">
                <CardHeader>
                  <CardTitle className="text-2xl">Quick Facts</CardTitle>
                  <div className="flex flex-wrap gap-6">
                    {listing.venues.tennis && listing.venues.tennis_total_courts && (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                          <path strokeWidth="2" d="M12 2v20M2 12h20"/>
                        </svg>
                        <span className="text-sm font-medium text-muted-foreground">
                          {listing.venues.tennis_total_courts} Tennis Court{listing.venues.tennis_total_courts > 1 ? 's' : ''}
                        </span>
                      </div>
                    )}
                    {listing.venues.padel && listing.venues.padel_total_courts && (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <rect x="3" y="3" width="18" height="18" rx="2" strokeWidth="2"/>
                          <path strokeWidth="2" d="M3 12h18M12 3v18"/>
                        </svg>
                        <span className="text-sm font-medium text-muted-foreground">
                          {listing.venues.padel_total_courts} Padel Court{listing.venues.padel_total_courts > 1 ? 's' : ''}
                        </span>
                      </div>
                    )}
                    {listing.venues.parking_spaces && (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeWidth="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
                          <path strokeWidth="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 001 1h5.5a1 1 0 001-1v-4.5"/>
                        </svg>
                        <span className="text-sm font-medium text-muted-foreground">
                          {listing.venues.parking_spaces} Parking Spaces
                        </span>
                      </div>
                    )}
                    {listing.venues.cafe && (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeWidth="2" d="M8 13h8M8 17h8M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                        </svg>
                        <span className="text-sm font-medium text-muted-foreground">Café</span>
                      </div>
                    )}
                    {listing.venues.wifi && (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeWidth="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
                        </svg>
                        <span className="text-sm font-medium text-muted-foreground">Free WiFi</span>
                      </div>
                    )}
                  </div>
                </CardHeader>
              </Card>
            )}
            
            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              
              {/* Main Content - Left Column (2/3 width) */}
              <div className="lg:col-span-2 space-y-8">
                
                {listing.summary && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-2xl">About</CardTitle>
                      <CardDescription className="text-base">
                        {listing.summary}
                      </CardDescription>
                    </CardHeader>
                  </Card>
                )}

                {/* Facilities */}
                {listing.venues && (
                  <div className="bg-card rounded-xl shadow-sm p-8">
                    <h2 className="text-2xl font-bold mb-6 text-card-foreground">What's Available</h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Tennis */}
                      {listing.venues.tennis && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                              <path strokeWidth="2" d="M12 2v20M2 12h20"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Tennis</h3>
                          </div>
                          {listing.venues.tennis_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.tennis_summary}</p>
                          )}
                          <div className="text-sm text-muted-foreground space-y-1">
                            {listing.venues.tennis_total_courts && (
                              <p className="font-semibold">{listing.venues.tennis_total_courts} courts</p>
                            )}
                            {listing.venues.tennis_indoor_courts && <p>• {listing.venues.tennis_indoor_courts} indoor</p>}
                            {listing.venues.tennis_outdoor_courts && <p>• {listing.venues.tennis_outdoor_courts} outdoor</p>}
                            {listing.venues.tennis_floodlit_courts && <p>• {listing.venues.tennis_floodlit_courts} floodlit</p>}
                          </div>
                        </div>
                      )}

                      {/* Padel */}
                      {listing.venues.padel && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <rect x="3" y="3" width="18" height="18" rx="2" strokeWidth="2"/>
                              <path strokeWidth="2" d="M3 12h18M12 3v18"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Padel</h3>
                          </div>
                          {listing.venues.padel_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.padel_summary}</p>
                          )}
                          {listing.venues.padel_total_courts && (
                            <p className="text-sm font-semibold text-muted-foreground">{listing.venues.padel_total_courts} courts</p>
                          )}
                        </div>
                      )}

                      {/* Pickleball */}
                      {listing.venues.pickleball && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Pickleball</h3>
                          </div>
                          {listing.venues.pickleball_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.pickleball_summary}</p>
                          )}
                          {listing.venues.pickleball_total_courts && (
                            <p className="text-sm font-semibold text-muted-foreground">{listing.venues.pickleball_total_courts} courts</p>
                          )}
                        </div>
                      )}

                      {/* Badminton */}
                      {listing.venues.badminton && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <circle cx="12" cy="12" r="3" strokeWidth="2"/>
                              <path strokeWidth="2" d="M12 2v4m0 12v4M2 12h4m12 0h4"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Badminton</h3>
                          </div>
                          {listing.venues.badminton_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.badminton_summary}</p>
                          )}
                          {listing.venues.badminton_total_courts && (
                            <p className="text-sm font-semibold text-muted-foreground">{listing.venues.badminton_total_courts} courts</p>
                          )}
                        </div>
                      )}

                      {/* Squash */}
                      {listing.venues.squash && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <rect x="4" y="4" width="16" height="16" rx="2" strokeWidth="2"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Squash</h3>
                          </div>
                          {listing.venues.squash_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.squash_summary}</p>
                          )}
                          <div className="text-sm text-muted-foreground space-y-1">
                            {listing.venues.squash_total_courts && (
                              <p className="font-semibold">{listing.venues.squash_total_courts} courts</p>
                            )}
                            {listing.venues.squash_glass_back_courts && <p>• {listing.venues.squash_glass_back_courts} glass-back</p>}
                          </div>
                        </div>
                      )}

                      {/* Swimming */}
                      {(listing.venues.indoor_pool || listing.venues.outdoor_pool) && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M5 12c1.5 0 2-1 3.5-1s2 1 3.5 1 2-1 3.5-1 2 1 3.5 1M5 18c1.5 0 2-1 3.5-1s2 1 3.5 1 2-1 3.5-1 2 1 3.5 1"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Swimming</h3>
                          </div>
                          {listing.venues.swimming_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.swimming_summary}</p>
                          )}
                          <div className="text-sm text-muted-foreground space-y-1">
                            {listing.venues.indoor_pool && (
                              <p>• Indoor pool{listing.venues.indoor_pool_length_m ? ` (${listing.venues.indoor_pool_length_m}m)` : ''}</p>
                            )}
                            {listing.venues.outdoor_pool && (
                              <p>• Outdoor pool{listing.venues.outdoor_pool_length_m ? ` (${listing.venues.outdoor_pool_length_m}m)` : ''}</p>
                            )}
                            {listing.venues.swimming_lessons && <p>• Lessons available</p>}
                          </div>
                        </div>
                      )}

                      {/* Gym */}
                      {listing.venues.gym_available && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M4.5 12h15m-15 0l3-3m-3 3l3 3m9-3l-3-3m3 3l-3 3"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Gym</h3>
                          </div>
                          {listing.venues.gym_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.gym_summary}</p>
                          )}
                          {listing.venues.gym_size && (
                            <p className="text-sm text-muted-foreground">Equipment stations: {listing.venues.gym_size}</p>
                          )}
                        </div>
                      )}

                      {/* Classes */}
                      {(listing.venues.classes_per_week || listing.venues.yoga_classes || listing.venues.pilates_classes) && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Classes</h3>
                          </div>
                          {listing.venues.classes_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.classes_summary}</p>
                          )}
                          <div className="text-sm text-muted-foreground space-y-1">
                            {listing.venues.classes_per_week && <p className="font-semibold">{listing.venues.classes_per_week}/week</p>}
                            {listing.venues.yoga_classes && <p>• Yoga</p>}
                            {listing.venues.pilates_classes && <p>• Pilates</p>}
                            {listing.venues.hiit_classes && <p>• HIIT</p>}
                          </div>
                        </div>
                      )}

                      {/* Spa */}
                      {listing.venues.spa_available && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Spa</h3>
                          </div>
                          {listing.venues.spa_summary && (
                            <p className="text-sm text-muted-foreground mb-2">{listing.venues.spa_summary}</p>
                          )}
                          <div className="text-sm text-muted-foreground space-y-1">
                            {listing.venues.sauna && <p>• Sauna</p>}
                            {listing.venues.steam_room && <p>• Steam room</p>}
                            {listing.venues.hot_tub && <p>• Hot tub</p>}
                          </div>
                        </div>
                      )}

                      {/* Parking */}
                      {listing.venues.parking_spaces && (
                        <div className="p-4 bg-secondary rounded-lg">
                          <div className="flex items-center gap-2 mb-2">
                            <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
                              <path strokeWidth="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 001 1h5.5a1 1 0 001-1v-4.5"/>
                            </svg>
                            <h3 className="font-bold text-lg text-card-foreground">Parking</h3>
                          </div>
                          <p className="text-sm font-semibold text-muted-foreground">{listing.venues.parking_spaces} spaces</p>
                          {listing.venues.ev_charging_available && (
                            <p className="text-sm text-muted-foreground">• EV charging</p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Opening Hours */}
                {listing.opening_hours && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-2xl">Opening Hours</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {Object.entries(listing.opening_hours as Record<string, any>).map(([day, hours]) => (
                          <div key={day} className="flex justify-between py-2 border-b last:border-b-0">
                            <span className="font-medium text-card-foreground capitalize">{day}</span>
                            <span className="text-muted-foreground">
                              {typeof hours === 'string' 
                                ? hours 
                                : hours && typeof hours === 'object' && 'open' in hours && 'close' in hours
                                  ? `${hours.open} - ${hours.close}`
                                  : 'Closed'}
                            </span>
                          </div>
                        ))}
                    </CardContent>
                  </Card>
                )}
                
              </div>

              {/* Sidebar - Right Column (1/3 width) */}
              <div className="lg:col-span-1 space-y-6">
                
                {/* Contact Card - Sticky */}
                <div className="bg-card rounded-xl shadow-sm p-6 sticky top-24">
                  <h2 className="text-xl font-bold mb-4 text-card-foreground">Get in Touch</h2>
                  
                  <div className="space-y-4">
                    {/* Website Button */}
                    {listing.website_url && (
                      <Button asChild className="w-full">
                        <a 
                          href={listing.website_url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Visit Website
                        </a>
                      </Button>
                    )}

                    {/* Phone */}
                    {listing.phone && (
                      <a 
                        href={`tel:${listing.phone}`}
                        className="flex items-center gap-3 text-muted-foreground hover:text-primary transition-colors group"
                      >
                        <div className="w-10 h-10 bg-secondary group-hover:bg-primary/20 rounded-lg flex items-center justify-center transition-colors">
                          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                          </svg>
                        </div>
                        <span className="font-medium">{listing.phone}</span>
                      </a>
                    )}

                    {/* Email */}
                    {listing.email && (
                      <a 
                        href={`mailto:${listing.email}`}
                        className="flex items-center gap-3 text-muted-foreground hover:text-primary transition-colors group"
                      >
                        <div className="w-10 h-10 bg-secondary group-hover:bg-primary/20 rounded-lg flex items-center justify-center transition-colors">
                          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                          </svg>
                        </div>
                        <span className="font-medium break-all">{listing.email}</span>
                      </a>
                    )}

                    {/* Address */}
                    {listing.street_address && (
                      <div className="pt-4">
                        <div className="flex gap-3">
                          <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center shrink-0">
                            <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                              <path strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                          </div>
                          <div className="text-sm text-muted-foreground">
                            <p>{listing.street_address}</p>
                            <p>{listing.city}</p>
                            <p className="font-semibold">{listing.postcode}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Map */}
                    {(listing.latitude && listing.longitude) && (
                      <Button asChild className="w-full">
                        <a
                          href={`https://www.google.com/maps/search/?api=1&query=${listing.latitude},${listing.longitude}`}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View on Google Maps
                        </a>
                      </Button>
                    )}

                    {/* Social Links */}
                    {(listing.instagram_url || listing.facebook_url || listing.twitter_url) && (
                      <div className="pt-4">
                        <h3 className="text-lg font-bold mb-3 text-card-foreground">Follow Us</h3>
                        <div className="flex gap-3">
                          {listing.instagram_url && (
                            <a 
                              href={listing.instagram_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="w-10 h-10 bg-secondary hover:bg-primary/20 rounded-lg flex items-center justify-center transition-colors group"
                              title="Instagram"
                            >
                              <FaInstagram className="w-5 h-5 text-primary group-hover:text-primary transition-colors" />
                            </a>
                          )}
                          {listing.facebook_url && (
                            <a 
                              href={listing.facebook_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="w-10 h-10 bg-secondary hover:bg-primary/20 rounded-lg flex items-center justify-center transition-colors group"
                              title="Facebook"
                            >
                              <FaFacebookF className="w-5 h-5 text-primary group-hover:text-primary transition-colors" />
                            </a>
                          )}
                          {listing.twitter_url && (
                            <a 
                              href={listing.twitter_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="w-10 h-10 bg-secondary hover:bg-primary/20 rounded-lg flex items-center justify-center transition-colors group"
                              title="Twitter"
                            >
                              <FaXTwitter className="w-5 h-5 text-primary group-hover:text-primary transition-colors" />
                            </a>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Categories */}
                {(listing.canonical_categories && listing.canonical_categories.length > 0) && (
                  <div className="bg-card rounded-xl shadow-sm p-6">
                    <h3 className="text-lg font-bold mb-3 text-card-foreground">Categories</h3>
                    <div className="flex flex-wrap gap-2">
                      {listing.canonical_categories.map((cat, index) => (
                        <a
                          key={index}
                          href={`/category/${cat}`}
                          className="bg-primary/20 hover:bg-primary/30 text-primary px-3 py-1.5 rounded-full text-sm font-medium transition-colors"
                        >
                          {categories[cat]?.name || cat}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </>
  )
}