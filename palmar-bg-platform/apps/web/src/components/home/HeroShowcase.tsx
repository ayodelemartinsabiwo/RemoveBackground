import { useState } from 'react'

export default function HeroShowcase() {
  return (
    <div className="relative flex justify-center items-center min-h-[800px] py-8 mt-12">
      {/* Left Demo Card - Portrait Precision */}
      <div className="absolute left-[-40px] top-[-5%] z-10 bg-white p-8 rounded-[20px] shadow-2xl animate-float">
        <span className="block text-lg font-semibold text-text-muted mb-4 text-center">
          Portrait Precision
        </span>
        <div className="demo-transition-container relative w-[320px] h-[480px] rounded-2xl overflow-hidden mb-4">
          <div className="demo-transition-image demo-image-with-bg bg-gray-100">
            <img
              src="/images/Background.jpg"
              alt="Portrait with background"
              className="w-[105%] h-[135%] mt-[30px] object-contain object-center"
            />
          </div>
          <div className="demo-transition-image demo-image-no-bg bg-checkerboard">
            <img
              src="/images/No_Background.png"
              alt="Portrait without background"
              className="w-[105%] h-[135%] mt-[30px] object-contain object-center"
            />
          </div>
          <div className="demo-transition-line" />
        </div>
        <span className="inline-block px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-light text-white rounded-[24px] text-base font-semibold">
          Perfect Hair Edges
        </span>
      </div>

      {/* Center Demo Card - Main/Overlapping */}
      <div className="absolute left-1/2 top-1/2 z-30 -translate-x-1/2 -translate-y-1/2 bg-white p-10 rounded-[20px] shadow-2xl animate-float-center">
        <div className="flex flex-row items-center gap-6">
          <div className="flex flex-col items-center">
            <span className="block text-lg font-semibold text-text-muted mb-4">Before</span>
            <div className="w-[280px] h-[400px] bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl flex items-center justify-center">
              <img
                src="/images/before.jpg"
                alt="Before - Image with background"
                className="w-full h-full object-contain rounded-2xl"
              />
            </div>
          </div>
          <div className="text-4xl text-primary-500 font-bold animate-arrow-bounce-h hidden md:block">
            →
          </div>
          <div className="text-4xl text-primary-500 font-bold animate-arrow-bounce-v md:hidden">
            ↓
          </div>
          <div className="flex flex-col items-center">
            <span className="block text-lg font-semibold text-text-muted mb-4">After</span>
            <div className="w-[280px] h-[400px] bg-checkerboard rounded-2xl flex items-end justify-center">
              <img
                src="/images/after.png"
                alt="After - Background removed"
                className="w-full h-full object-contain object-bottom rounded-2xl"
              />
            </div>
            <span className="inline-block mt-4 px-6 py-3 bg-gradient-to-r from-primary-500 via-primary-light to-yellow-400 text-white rounded-[24px] text-base font-semibold">
              Crystal Clear
            </span>
          </div>
        </div>
      </div>

      {/* Right Demo Card - Product Precision */}
      <div className="absolute right-[-40px] top-[30%] z-20 bg-white p-8 rounded-[20px] shadow-2xl animate-float-delayed">
        <span className="block text-lg font-semibold text-text-muted mb-4 text-center">
          Product Precision
        </span>
        <div className="demo-transition-container relative w-[320px] h-[400px] rounded-2xl overflow-hidden mb-4">
          <div className="demo-transition-image demo-image-with-bg" style={{ background: '#D2CCC0' }}>
            <img
              src="/images/right_background.jpg"
              alt="Product with background"
              className="w-[105%] h-[135%] object-contain object-center"
            />
          </div>
          <div className="demo-transition-image demo-image-no-bg bg-checkerboard">
            <img
              src="/images/right_no_background2.png"
              alt="Product without background"
              className="w-[105%] h-[135%] object-contain object-center"
            />
          </div>
          <div className="demo-transition-line" />
        </div>
        <span className="inline-block px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-light text-white rounded-[24px] text-base font-semibold">
          Sharp Details
        </span>
        <div className="text-[10px] text-gray-400 text-center mt-3 leading-tight">
          Photo by{' '}
          <a
            href="https://unsplash.com/@ayomikun93?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-primary-500 transition-colors"
          >
            Ayomikun Barry
          </a>{' '}
          on{' '}
          <a
            href="https://unsplash.com/photos/a-person-is-holding-a-stylish-brown-purse--WbdCEVIlTM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-primary-500 transition-colors"
          >
            Unsplash
          </a>
        </div>
      </div>
    </div>
  )
}
