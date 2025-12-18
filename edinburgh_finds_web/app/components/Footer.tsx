export default function Footer() {
  return (
    <footer className="bg-slate-900 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm">
            © 2025 Edinburgh Finds
          </p>
          <p className="text-sm">
            <a 
              href="mailto:hello@edinburghfinds.co.uk"
              className="hover:text-teal-400 transition-colors"
            >
              hello@edinburghfinds.co.uk
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}