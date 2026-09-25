import React from "react";
import { motion } from "framer-motion";
import bandaiNamcoLogo from "../../assets/partners/bandai-namco-logo-web-desktop.svg";
import goodSmileLogo from "../../assets/partners/goodsmile.svg";
import lezhinLogo from "../../assets/partners/lezhin.svg";
import wlsLogo from "../../assets/partners/wls-lg.svg";
import mantaLogo from "../../assets/partners/manta-logo-brand_71x18.webp";
import bookwalkerLogo from "../../assets/partners/bookwalker.svg";
import tappytoonLogo from "../../assets/partners/tappytoon.svg";
import tapasLogo from "../../assets/partners/tapas.jpg";
import rentaLogo from "../../assets/partners/renta.svg";

export default function PartnerMarquee() {
  const partners = [
    {
      name: "BANDAI NAMCO",
      logo: bandaiNamcoLogo.src,
      width: 160,
      height: 32,
    },
    {
      name: "GOOD SMILE",
      logo: goodSmileLogo.src,
      width: 140,
      height: 32,
    },
    {
      name: "LEZHIN",
      logo: lezhinLogo.src,
      width: 120,
      height: 32,
    },
    {
      name: "WLS",
      logo: wlsLogo.src,

      width: 100,
      height: 32,
    },
    {
      name: "Manta",
      logo: mantaLogo.src,

      width: 100,
      height: 32,
    },
    {
      name: "Bookwalker",
      logo: bookwalkerLogo.src,

      width: 100,
      height: 32,
      filter: "drop-shadow(0px 0px 20px white)",
    },
    {
      name: "Tappy Toon",
      logo: tappytoonLogo.src,

      width: 100,
      height: 25,
      filter: "drop-shadow(0px 0px 10px white)",
    },
    {
      name: "Tapas",
      logo: tapasLogo.src,

      width: 100,
      height: 32,
    },
    {
      name: "Renta",
      logo: rentaLogo.src,

      width: 100,
      height: 32,
    },
  ];

  // Duplicate set for seamless continuous marquee loop
  const marqueeItems = [...partners, ...partners];

  return (
    <section
      aria-label="Official Partners & Contributors"
      className="relative overflow-hidden bg-surface/50 backdrop-blur-sm border-b border-white/5 py-12"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <h2 className="text-xs uppercase tracking-widest text-porcelain/75 font-mono">
          Official Partners & Contributors
        </h2>
      </div>

      <div className="flex w-full select-none">
        <motion.div
          animate={{ x: ["0%", "-25%"] }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="flex gap-8 min-w-max px-4"
        >
          {marqueeItems.map((partner, idx) => {
            const isDuplicate = idx >= partners.length;
            return (
              <motion.div
                key={`${partner.name}-${idx}`}
                whileHover={{ y: -4, scale: 1.02 }}
                aria-hidden={isDuplicate ? "true" : undefined}
                className="flex flex-col items-center justify-center gap-3 px-8 py-6 rounded-xl card-glass hover:border-razzmatazz/30 transition-all whitespace-nowrap min-w-max"
              >
                <img
                  src={partner.logo}
                  alt={isDuplicate ? "" : partner.name}
                  width={partner.width}
                  height={partner.height}
                  loading="lazy"
                  decoding="async"
                  style={{filter:partner.filter ?? ""}}
                  className="h-8 w-auto object-contain transition-all duration-500"
                />
                <div className="flex flex-col items-center gap-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-porcelain">
                    {partner.name}
                  </span>
                  {/*<span className="text-[9px] text-porcelain/75 uppercase tracking-tighter font-medium">
                    {partner.tagline}
                  </span>*/}
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
