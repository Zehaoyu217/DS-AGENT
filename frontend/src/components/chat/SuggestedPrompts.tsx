import { AlertTriangle, BarChart2, Users, TrendingUp } from 'lucide-react'

interface Prompt {
  icon: React.ElementType
  label: string
  text: string
}

const PROMPTS: Prompt[] = [
  {
    icon: Users,
    label: 'Segment credit & balance profile',
    text: "Profile the three customer segments (retail, business, premium). For each: average credit score, average account balance, and number of active accounts. Show a grouped bar chart.",
  },
  {
    icon: AlertTriangle,
    label: 'Flag anomaly investigation',
    text: 'List all flagged transactions with customer name, segment, amount, category, and counterparty. Rank by absolute amount. Which flagged patterns look like genuine fraud vs false positives?',
  },
  {
    icon: BarChart2,
    label: 'Loan default risk by region',
    text: 'Calculate default and delinquency rates by region and loan type. Show a heatmap. Which region+loan_type combination has the highest default risk?',
  },
  {
    icon: TrendingUp,
    label: 'Rate sensitivity on loan portfolio',
    text: 'Join loans with daily_rates to estimate how the two fed rate cuts in 2025 (June 15 and Sep 15) affected the average new-loan interest rate. Plot the monthly average loan rate alongside fed_funds_rate.',
  },
]

interface SuggestedPromptsProps {
  onSelect: (text: string) => void
}

export function SuggestedPrompts({ onSelect }: SuggestedPromptsProps) {
  return (
    <div className="flex flex-col border border-surface-700/50 divide-y divide-surface-700/50">
      {PROMPTS.map((p) => {
        const Icon = p.icon
        return (
          <button
            key={p.label}
            onClick={() => onSelect(p.text)}
            className="flex items-center gap-3 px-4 py-2.5 bg-transparent hover:bg-surface-800/60 text-left transition-colors group"
          >
            <Icon
              className="w-3.5 h-3.5 text-brand-accent-hover flex-shrink-0 group-hover:text-brand-400 transition-colors"
              aria-hidden
            />
            <div className="min-w-0">
              <p className="text-[11px] font-mono text-surface-400 group-hover:text-surface-200 transition-colors">
                {p.label}
              </p>
            </div>
          </button>
        )
      })}
    </div>
  )
}
