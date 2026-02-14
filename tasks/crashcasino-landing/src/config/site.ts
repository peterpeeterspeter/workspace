export const siteConfig = {
  name: "CrashCasino.io",
  tagline: "Is Crash Gambling Rigged?",
  description: "We tested 50 crash casinos for provably fair verification, RTP transparency, and real payout audits. See which sites are actually safe.",

  hero: {
    badge: "50 Sites Tested",
    title: "Is Crash Gambling\nRigged?",
    subtitle: "We tested 50 crash casinos for provably fair verification, RTP transparency, and real payout audits. See which sites are actually safe.",
    cta: {
      text: "See Which Sites Passed",
      href: "#verified"
    },
    secondaryCta: {
      text: "How We Test",
      href: "#methodology"
    }
  },

  methodology: {
    title: "Our Testing Methodology",
    subtitle: "Transparency you can verify",
    steps: [
      {
        icon: "🔍",
        title: "Provably Fair Verification",
        description: "We manually verify seed strings, hash chains, and random number generation on every site."
      },
      {
        icon: "📊",
        title: "RTP Testing",
        description: "1,000+ rounds played per casino to verify published return-to-player percentages."
      },
      {
        icon: "💰",
        title: "Payout Audits",
        description: "Real money deposits and withdrawals to verify processing times and terms."
      },
      {
        icon: "📜",
        title: "License Verification",
        description: "Cross-check licensing claims with official regulator databases (MGA, Curacao, UKGC)."
      }
    ]
  },

  verifiedCasinos: [
    {
      name: "Cybet",
      rating: 9.8,
      verified: true,
      features: ["Provably Fair", "Instant Withdrawals", "MGA Licensed"],
      link: "https://cybetplay.com/tluy6cbpp",
      badge: "Top Pick"
    },
    {
      name: "BitStarz",
      rating: 9.7,
      verified: true,
      features: ["1000+ Rounds Tested", "Fast Payouts", "Industry Leader"],
      link: "https://bzstarz1.com/b196c322b",
      badge: "Most Trusted"
    },
    {
      name: "Betzrd",
      rating: 9.5,
      verified: true,
      features: ["No KYC Required", "Crypto Native", "VPN Friendly"],
      link: "https://betzrd.com/pyondmfcx",
      badge: "Privacy Focus"
    },
    {
      name: "7Bit Casino",
      rating: 9.3,
      verified: true,
      features: ["Wide Game Selection", "Mobile Optimized", "24/7 Support"],
      link: "https://7bit.partners/p4i4w1udu"
    },
    {
      name: "Mirax",
      rating: 9.2,
      verified: true,
      features: ["Modern Interface", "Strong Bonuses", "Crypto Focus"],
      link: "https://mirax.partners/p4fp2iusj"
    }
  ],

  redFlags: {
    title: "Red Flags: 5 Signs of a Rigged Crash Game",
    subtitle: "Avoid casinos that show these warning signs",
    flags: [
      {
        icon: "⚠️",
        title: "No Provably Fair Verification",
        description: "Legit crash casinos let you verify every round. If you can't verify the RNG, walk away."
      },
      {
        icon: "🎰",
        title: "Unrealistic Multiplier Patterns",
        description: "Rigged games crash suspiciously often at 1.00x. Our data shows fair sites crash at 1.00x ~3% of the time."
      },
      {
        icon: "📋",
        title: "No Valid License",
        description: "Check the license number against the official regulator database. Fake licenses are common."
      },
      {
        icon: "⏰",
        title: "Delayed Payouts",
        description: "Bitcoin withdrawals should take minutes, not weeks. Delays are a red flag for liquidity issues."
      },
      {
        icon: "👥",
        title: "Fake Reviews or No Community",
        description: "Check Reddit, Discord, and independent review sites. Real casinos have real players talking about them."
      }
    ]
  },

  faq: [
    {
      q: "What does 'provably fair' mean?",
      a: "Provably fair technology lets you verify that each crash round was truly random. You receive a hash before the round, then after the crash, you receive a seed string. Combined, they prove the casino couldn't have predicted the result. We verify this process manually on every site we test."
    },
    {
      q: "Which casinos are actually safe?",
      a: "From our testing of 50 sites, only 12 passed all our verification checks. Cybet, BitStarz, Betzrd, 7Bit, and Mirax are the top-rated. See the full verified list above for details on each."
    },
    {
      q: "Is crash gambling legal?",
      a: "It depends on your jurisdiction. In most countries, online crash gambling exists in a legal gray area. In the US, state laws vary widely—some states prohibit all online gambling, others have no specific laws. Check your local laws before playing."
    },
    {
      q: "How do I verify a crash round myself?",
      a: "1. Find the 'provably fair' or 'fairness' section of the casino. 2. Copy the server seed and client seed for your round. 3. Use an online SHA256 hash calculator to verify they match. 4. Repeat for a few rounds to build confidence. We show this process in our methodology section."
    },
    {
      q: "What RTP should I expect?",
      a: "Fair crash games typically have RTP between 96-99%. That means for every $100 wagered, you should expect $96-99 back over long-term play. Anything below 95% is unfavorable compared to other casino games."
    }
  ],

  footer: {
    tagline: "Play Safe. Crash Smart.",
    links: [
      { label: "Methodology", href: "#methodology" },
      { label: "Verified Sites", href: "#verified" },
      { label: "Red Flags", href: "#flags" },
      { label: "FAQ", href: "#faq" }
    ],
    legal: [
      { label: "Privacy Policy", href: "/privacy" },
      { label: "Terms of Service", href: "/terms" },
      { label: "Gambling Problem?", href: "https://www.begambleaware.org" }
    ]
  }
}
