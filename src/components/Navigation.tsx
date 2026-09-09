import React, { useState, useRef } from 'react';
import { Menu, X, Search } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const desktopSearchInputRef = useRef<HTMLInputElement>(null);
  const mobileSearchInputRef = useRef<HTMLInputElement>(null);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/posts/search?q=${encodeURIComponent(searchQuery.trim())}`;
    } else {
      // Focus desktop or mobile search bar if empty when user clicks search icon
      if (window.innerWidth >= 640) {
        desktopSearchInputRef.current?.focus();
      } else {
        mobileSearchInputRef.current?.focus();
      }
    }
  };

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Podcasts', href: '/podcasts' },
    { name: 'Posts', href: '/posts' },
    { name: 'Contact', href: '/contact' },
  ];

  return (
    <>
      {/* Floating Glass Header */}
      <motion.header
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 md:h-20">
            {/* Logo with Heartbeat Throb Effect */}
            <motion.a
              href="/"
              whileHover={{
                scale: [1, 1.08, 0.98, 1.06, 1],
              }}
              transition={{
                duration: 0.8,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="flex items-center gap-2 group cursor-pointer"
            >
              <span className="text-lg md:text-xl font-black tracking-wider uppercase select-none">
                <span className="text-porcelain">ZEALED</span>
                <span className="text-razzmatazz">FUJOSHI</span>
              </span>
            </motion.a>

            {/* Desktop Navigation */}
            <nav class="hidden md:flex items-center gap-8" aria-label="Main Navigation">
              {navLinks.map((link) => (
                <motion.a
                  key={link.name}
                  href={link.href}
                  whileHover={{ y: -2 }}
                  className="text-xs uppercase tracking-wider text-white/70 hover:text-white transition-colors border-b-2 border-transparent hover:border-[#FF1177] pb-1"
                >
                  {link.name}
                </motion.a>
              ))}
            </nav>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-2">
                <form onSubmit={handleSearchSubmit} className="relative group" role="search">
                  <input
                    ref={desktopSearchInputRef}
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search posts..."
                    aria-label="Search posts"
                    className="bg-white/5 border border-white/10 rounded-lg px-3 py-1.5 text-xs text-white placeholder-white/30 focus:outline-none focus:ring-1 focus:ring-[#FF1177] transition-all w-40 opacity-100"
                  />
                  <button 
                    type="submit" 
                    aria-label="Submit search or focus search input"
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:text-[#FF1177] transition-colors cursor-pointer"
                  >
                    <Search size={14} className="text-white/50" />
                  </button>
                </form>
              </div>

              {/* Mobile Menu Button */}
              <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                aria-label={isOpen ? "Close menu" : "Open navigation menu"}
                aria-expanded={isOpen}
                className="md:hidden p-2 hover:bg-white/5 rounded-lg transition cursor-pointer"
              >
                {isOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <motion.div
          initial={false}
          animate={{ height: isOpen ? 'auto' : 0 }}
          transition={{ duration: 0.3 }}
          className="md:hidden overflow-hidden bg-black/80 backdrop-blur-xl border-t border-white/5"
        >
          <div className="px-4 py-4 space-y-3">
            <form onSubmit={handleSearchSubmit} className="relative mb-4" role="search">
              <input
                ref={mobileSearchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search posts..."
                aria-label="Search posts"
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:ring-1 focus:ring-[#FF1177]"
              />
              <button 
                type="submit" 
                aria-label="Submit search"
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-white/50 hover:text-white cursor-pointer"
              >
                <Search size={18} />
              </button>
            </form>
            <nav aria-label="Mobile Navigation" className="space-y-3">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  className="block text-sm uppercase tracking-wider text-white/70 hover:text-white hover:pl-2 transition-all"
                  onClick={() => setIsOpen(false)}
                >
                  {link.name}
                </a>
              ))}
            </nav>
          </div>
        </motion.div>
      </motion.header>

      {/* Spacer */}
      <div className="h-16 md:h-20" />
    </>
  );
}