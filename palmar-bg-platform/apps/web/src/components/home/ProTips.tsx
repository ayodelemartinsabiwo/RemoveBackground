import { useState } from 'react'

interface TipCardProps {
  icon: string
  title: string
  titleBack: string
  content: string
}

function TipCard({ icon, title, titleBack, content }: TipCardProps) {
  const [isFlipped, setIsFlipped] = useState(false)

  return (
    <div
      className={`tip-card h-[300px] cursor-pointer ${isFlipped ? 'flipped' : ''}`}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className="tip-card-inner">
        <div className="tip-card-front shadow-lg">
          <div className="text-6xl mb-4">{icon}</div>
          <h3 className="text-2xl font-semibold mb-2 text-text-dark">{title}</h3>
          <p className="text-sm text-text-muted italic">Click to learn more</p>
        </div>
        <div className="tip-card-back shadow-lg">
          <h3 className="text-xl font-bold mb-4">{titleBack}</h3>
          <p className="text-[0.95rem] leading-relaxed opacity-95">{content}</p>
        </div>
      </div>
    </div>
  )
}

export default function ProTips() {
  const tips = [
    {
      icon: '📸',
      title: 'Image Quality',
      titleBack: 'Use High-Resolution Images',
      content: 'For optimal results, use images with at least 1920x1080 resolution. Higher resolution provides more detail for the AI to work with, resulting in cleaner edges and better subject separation.',
    },
    {
      icon: '🎯',
      title: 'Clean Backgrounds',
      titleBack: 'Minimize Background Noise',
      content: 'Images with less cluttered backgrounds process better. If possible, choose photos with clear subject-background separation. Plain or contrasting backgrounds yield the most precise results.',
    },
    {
      icon: '💡',
      title: 'Lighting Matters',
      titleBack: 'Good Lighting = Better Results',
      content: 'Well-lit images with even lighting across the subject produce superior results. Avoid heavy shadows or extreme backlighting, as these can confuse edge detection.',
    },
    {
      icon: '🔍',
      title: 'Subject Focus',
      titleBack: 'Sharp Focus on Subject',
      content: 'Ensure your main subject is in sharp focus. Blurry or out-of-focus images make it harder for the AI to distinguish edges accurately, especially with fine details like hair.',
    },
    {
      icon: '🎨',
      title: 'Color Contrast',
      titleBack: 'Strong Subject-Background Contrast',
      content: 'Images where the subject\'s colors differ significantly from the background are easier to process. Avoid subjects wearing colors that blend with the background.',
    },
    {
      icon: '⚡',
      title: 'File Formats',
      titleBack: 'Choose Quality Formats',
      content: 'Use PNG or high-quality JPG formats for input. Heavily compressed images may have artifacts that affect edge precision. The output is always saved as high-quality transparent PNG.',
    },
  ]

  return (
    <section className="py-24 bg-gradient-to-br from-bg-light via-gray-100 to-bg-light">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-text-dark mb-4">Pro Tips for Best Results</h2>
          <p className="text-lg text-text-light max-w-2xl mx-auto">
            Click each card to discover expert techniques
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {tips.map((tip, index) => (
            <TipCard key={index} {...tip} />
          ))}
        </div>
      </div>
    </section>
  )
}
