import { Link } from 'react-router-dom'
import { Check, X } from 'lucide-react'
import Header from '@/components/common/Header'
import Footer from '@/components/common/Footer'

export default function PricingPage() {
  const plans = [
    {
      name: 'FREE',
      price: '$0',
      credits: 3,
      period: 'One-time',
      features: [
        { text: '3 Credits (one-time)', included: true },
        { text: 'Small resolution downloads (512px)', included: true },
        { text: 'Background customization', included: true },
        { text: 'Cloud storage (7 days)', included: true },
        { text: 'HD resolution downloads', included: false },
        { text: 'Ultra-HD resolution downloads', included: false },
      ],
      cta: 'Get Started',
      link: '/register',
      highlight: false,
    },
    {
      name: 'STARTER',
      price: '$9',
      credits: 40,
      period: 'Monthly',
      features: [
        { text: '40 Credits per month', included: true },
        { text: 'Small + HD downloads (1920px)', included: true },
        { text: 'Background customization', included: true },
        { text: 'Cloud storage (30 days)', included: true },
        { text: 'Priority processing', included: true },
        { text: 'Ultra-HD resolution downloads', included: false },
      ],
      cta: 'Start Free Trial',
      link: '/register',
      highlight: false,
    },
    {
      name: 'PROFESSIONAL',
      price: '$19',
      credits: 120,
      period: 'Monthly',
      features: [
        { text: '120 Credits per month', included: true },
        { text: 'Small + HD + Ultra-HD (3840px)', included: true },
        { text: 'Advanced background customization', included: true },
        { text: 'Cloud storage (90 days)', included: true },
        { text: 'Priority processing', included: true },
        { text: 'Email support', included: true },
      ],
      cta: 'Start Free Trial',
      link: '/register',
      highlight: true,
    },
    {
      name: 'BUSINESS',
      price: '$49',
      credits: 350,
      period: 'Monthly',
      features: [
        { text: '350 Credits per month', included: true },
        { text: 'All resolution downloads', included: true },
        { text: 'Advanced customization + API access', included: true },
        { text: 'Cloud storage (1 year)', included: true },
        { text: 'Priority processing + Batch upload', included: true },
        { text: 'Priority email support', included: true },
      ],
      cta: 'Start Free Trial',
      link: '/register',
      highlight: false,
    },
    {
      name: 'ENTERPRISE',
      price: '$99',
      credits: 850,
      period: 'Monthly',
      features: [
        { text: '850 Credits per month', included: true },
        { text: 'All resolution downloads', included: true },
        { text: 'Full API access + Webhooks', included: true },
        { text: 'Cloud storage (unlimited)', included: true },
        { text: 'Fastest processing + Bulk operations', included: true },
        { text: 'Dedicated support + SLA', included: true },
      ],
      cta: 'Contact Sales',
      link: '/register',
      highlight: false,
    },
    {
      name: 'ULTRA',
      price: '$199',
      credits: 5000,
      period: 'Monthly',
      features: [
        { text: '5000 Credits per month', included: true },
        { text: 'All resolution downloads', included: true },
        { text: 'Full API + Custom integrations', included: true },
        { text: 'Cloud storage (unlimited)', included: true },
        { text: 'Maximum speed + White-label options', included: true },
        { text: 'Dedicated account manager', included: true },
      ],
      cta: 'Contact Sales',
      link: '/register',
      highlight: false,
    },
  ]

  const lifetimePlans = [
    {
      name: 'STARTER LIFETIME',
      price: '$199',
      credits: 10,
      features: [
        { text: '10 Lifetime credits', included: true },
        { text: 'Small + HD downloads', included: true },
        { text: 'Background customization', included: true },
        { text: 'Cloud storage (1 year)', included: true },
      ],
    },
    {
      name: 'PROFESSIONAL LIFETIME',
      price: '$399',
      credits: 50,
      features: [
        { text: '50 Lifetime credits', included: true },
        { text: 'All resolution downloads', included: true },
        { text: 'Advanced customization', included: true },
        { text: 'Cloud storage (unlimited)', included: true },
      ],
    },
    {
      name: 'BUSINESS LIFETIME',
      price: '$799',
      credits: 150,
      features: [
        { text: '150 Lifetime credits', included: true },
        { text: 'All resolutions + API access', included: true },
        { text: 'Advanced customization', included: true },
        { text: 'Cloud storage (unlimited)', included: true },
      ],
    },
    {
      name: 'ENTERPRISE LIFETIME',
      price: '$1,599',
      credits: 500,
      features: [
        { text: '500 Lifetime credits', included: true },
        { text: 'Full API + Webhooks', included: true },
        { text: 'Custom integrations', included: true },
        { text: 'Priority support + SLA', included: true },
      ],
    },
  ]

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero */}
      <section className="bg-gradient-to-br from-primary-50 to-orange-50 py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Choose Your Perfect Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Flexible pricing for individuals, professionals, and enterprises.
            Start free or choose a plan that grows with your needs.
          </p>
        </div>
      </section>

      {/* Monthly Plans */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Monthly Plans</h2>
            <p className="text-lg text-gray-600">
              Flexible credit-based plans with cloud storage and multi-device access
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {plans.map((plan) => (
              <div
                key={plan.name}
                className={`rounded-2xl p-8 ${
                  plan.highlight
                    ? 'bg-gradient-to-br from-primary-500 to-orange-500 text-white shadow-2xl scale-105'
                    : 'bg-white border-2 border-gray-200'
                }`}
              >
                <div className="text-center mb-6">
                  <h3 className={`text-2xl font-bold mb-2 ${plan.highlight ? 'text-white' : 'text-gray-900'}`}>
                    {plan.name}
                  </h3>
                  <div className={`text-5xl font-bold mb-2 ${plan.highlight ? 'text-white' : 'text-primary-500'}`}>
                    {plan.price}
                  </div>
                  <div className={plan.highlight ? 'text-white/90' : 'text-gray-600'}>
                    {plan.period}
                  </div>
                  <div className={`text-lg font-semibold mt-2 ${plan.highlight ? 'text-white' : 'text-gray-700'}`}>
                    {plan.credits} Credits
                  </div>
                </div>

                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      {feature.included ? (
                        <Check className={`w-5 h-5 flex-shrink-0 mt-0.5 ${plan.highlight ? 'text-white' : 'text-green-500'}`} />
                      ) : (
                        <X className={`w-5 h-5 flex-shrink-0 mt-0.5 ${plan.highlight ? 'text-white/50' : 'text-gray-400'}`} />
                      )}
                      <span className={feature.included ? '' : 'line-through opacity-50'}>
                        {feature.text}
                      </span>
                    </li>
                  ))}
                </ul>

                <Link
                  to={plan.link}
                  className={`block text-center w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                    plan.highlight
                      ? 'bg-white text-primary-600 hover:bg-gray-100'
                      : 'bg-primary-500 text-white hover:bg-primary-600'
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Lifetime Plans */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Lifetime Plans</h2>
            <p className="text-lg text-gray-600">
              One-time purchase with lifetime credits for the web platform
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
            {lifetimePlans.map((plan) => (
              <div key={plan.name} className="bg-white rounded-xl p-6 border-2 border-gray-200 hover:border-primary-500 transition-colors">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="text-4xl font-bold text-primary-500 mb-4">{plan.price}</div>
                <div className="text-sm text-gray-600 mb-6">{plan.credits} Lifetime Credits</div>

                <ul className="space-y-2 mb-6">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                      <Check className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                      <span>{feature.text}</span>
                    </li>
                  ))}
                </ul>

                <Link
                  to="/register"
                  className="block text-center w-full py-2 px-4 bg-primary-500 text-white rounded-lg font-semibold hover:bg-primary-600 transition-colors"
                >
                  Purchase
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Desktop CTA */}
      <section className="py-20 bg-gradient-to-br from-gray-900 to-gray-800 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Need Unlimited Processing?</h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Get the Desktop version for a one-time payment of $320.95 with unlimited offline processing
          </p>
          <a
            href="https://github.com/ayodelemartinsabiwo/RemoveBackground/releases"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-4 bg-primary-500 text-white font-semibold rounded-lg hover:bg-primary-600 transition-colors shadow-lg text-lg"
          >
            Learn About Desktop Version
          </a>
        </div>
      </section>

      <Footer />
    </div>
  )
}
