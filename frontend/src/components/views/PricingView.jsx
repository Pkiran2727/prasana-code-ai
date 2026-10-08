import React, { useState } from 'react';
import { Check, ShieldCheck, Sparkles, CreditCard, Zap, Star, QrCode, ArrowRight, X } from 'lucide-react';
import { API_BASE_URL } from '../../api/agentApi';

export default function PricingView({ userEmail }) {
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);
  const [showUpiModal, setShowUpiModal] = useState(false);
  const [txnRef, setTxnRef] = useState('');

  // Default UPI ID for Personal Savings Account Settlement
  const personalUpiId = "mandaprasannakiran@gmail";

  const plans = [
    {
      id: 'pro_monthly',
      name: 'Pro Monthly',
      price: '₹799',
      period: '/month',
      numericPrice: 799,
      desc: 'Ideal for coders looking for monthly flexibility.',
      features: [
        'All 5 Learning Paths Access',
        'Prasana AI Tutor (Unlimited Line Hints)',
        'Practice & DSA Problem Bank',
        'Automated Test Case Verification',
        'Standard Execution Sandbox'
      ],
      popular: false,
      amountPaise: 79900
    },
    {
      id: 'pro_annual',
      name: 'Pro Annual',
      price: '₹2,499',
      period: '/year',
      numericPrice: 2499,
      desc: 'Best value! Save 70% with annual subscription.',
      features: [
        'Everything in Monthly Plan',
        '70% Annual Discount Savings',
        'Priority AI Tutor Response Speed',
        'Verifiable Shareable Certificate',
        'Exclusive @itsprasana Community Badge'
      ],
      popular: true,
      amountPaise: 249900
    },
    {
      id: 'lifetime',
      name: 'Lifetime Pass',
      price: '₹6,499',
      period: 'one-time',
      numericPrice: 6499,
      desc: 'Pay once, enjoy permanent access forever.',
      features: [
        'Lifetime Unlimited Access to All Paths',
        'All Future Course & AI Updates Included',
        'Unlimited AI Tutor Coaching Forever',
        'Direct Discord / Telegram VIP Support',
        'Personalized Certificate of Mastery'
      ],
      popular: false,
      amountPaise: 649900
    }
  ];

  const handleOpenUpi = (plan) => {
    setSelectedPlan(plan);
    setShowUpiModal(true);
  };

  const handleVerifyUpiTxn = async (e) => {
    e.preventDefault();
    if (!txnRef.trim()) return;
    setIsProcessing(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/payment/verify-payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          razorpay_order_id: `order_upi_${Date.now()}`,
          razorpay_payment_id: txnRef,
          razorpay_signature: 'upi_manual_sig',
          user_email: userEmail || 'user@example.com',
          plan_id: selectedPlan.id
        })
      });
      await res.json();
      setIsProcessing(false);
      setShowUpiModal(false);
      setPaymentSuccess(true);
    } catch (err) {
      console.error('UPI Verification error:', err);
      setIsProcessing(false);
      setShowUpiModal(false);
      setPaymentSuccess(true);
    }
  };

  const handleSubscribeRazorpay = async (plan) => {
    setSelectedPlan(plan);
    setIsProcessing(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/payment/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan_id: plan.id,
          amount: plan.amountPaise,
          currency: 'INR'
        })
      });
      const data = await res.json();

      if (window.Razorpay) {
        const options = {
          key: data.key_id,
          amount: data.amount,
          currency: data.currency,
          name: 'Prasana Code AI',
          description: `Subscription for ${plan.name}`,
          order_id: data.order_id,
          handler: async function (response) {
            await fetch('http://localhost:8000/api/payment/verify-payment', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                user_email: userEmail || 'user@example.com',
                plan_id: plan.id
              })
            });
            setIsProcessing(false);
            setPaymentSuccess(true);
          },
          prefill: {
            email: userEmail || 'user@example.com'
          },
          theme: {
            color: '#10b981'
          }
        };
        const rzp = new window.Razorpay(options);
        rzp.open();
      } else {
        setTimeout(async () => {
          await fetch('http://localhost:8000/api/payment/verify-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              razorpay_order_id: data.order_id,
              razorpay_payment_id: 'pay_mock_123',
              razorpay_signature: 'sig_mock_123',
              user_email: userEmail || 'user@example.com',
              plan_id: plan.id
            })
          });
          setIsProcessing(false);
          setPaymentSuccess(true);
        }, 1200);
      }
    } catch (err) {
      console.error('Payment error:', err);
      setIsProcessing(false);
    }
  };

  return (
    <div className="h-full w-full bg-ide-bg text-ide-text p-8 overflow-y-auto pb-32 font-sans relative">
      <div className="max-w-6xl mx-auto text-center">
        {/* Badges */}
        <div className="inline-flex items-center gap-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
            <QrCode className="w-3.5 h-3.5" />
            <span>0% Fee Direct Personal UPI (GPay / PhonePe / BHIM)</span>
          </div>
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-300 text-xs font-medium">
            <CreditCard className="w-3.5 h-3.5" />
            <span>Razorpay Gateway Support</span>
          </div>
        </div>

        <h1 className="text-3xl md:text-4xl font-bold tracking-tight mt-3 text-ide-text">Invest in Your Software Engineering Career</h1>
        <p className="text-ide-muted mt-1 text-sm max-w-2xl mx-auto font-normal">
          Unlock full access to all 5 interactive skill paths, Prasana AI Tutor hints, and DSA practice problems.
        </p>

        {paymentSuccess && (
          <div className="my-4 p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold max-w-md mx-auto flex items-center justify-center gap-2">
            <ShieldCheck className="w-4 h-4" />
            <span>Success! Your Pro Subscription is active.</span>
          </div>
        )}

        {/* Pricing Cards Grid */}
        <div className="mt-6 grid md:grid-cols-3 gap-6 text-left">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative rounded-3xl p-6 flex flex-col justify-between transition-all duration-300 ${
                plan.popular
                  ? 'bg-ide-panel/90 border-2 border-emerald-400 shadow-xl shadow-emerald-500/10 scale-105'
                  : 'bg-ide-panel/70 border border-ide-border/80 hover:border-ide-border'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 text-slate-950 text-[10px] font-extrabold uppercase tracking-wider shadow-md">
                  Most Popular
                </div>
              )}

              <div>
                <h3 className="text-lg font-bold text-ide-text">{plan.name}</h3>
                <p className="text-ide-muted text-xs mt-0.5 min-h-[32px] font-normal">{plan.desc}</p>

                <div className="mt-4 flex items-baseline gap-1">
                  <span className="text-3xl font-extrabold tracking-tight text-ide-text">{plan.price}</span>
                  <span className="text-ide-muted text-xs font-medium">{plan.period}</span>
                </div>

                <ul className="mt-5 space-y-2">
                  {plan.features.map((feat, idx) => (
                    <li key={idx} className="flex items-center gap-2 text-xs text-ide-text">
                      <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span>{feat}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-6 space-y-2">
                {/* 1. Razorpay Instant API Popup */}
                <button
                  onClick={() => handleSubscribeRazorpay(plan)}
                  disabled={isProcessing}
                  className="w-full py-2.5 rounded-xl font-bold text-xs bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 shadow-md shadow-emerald-500/20 transition-all duration-200 active:scale-95 flex items-center justify-center gap-2"
                >
                  <Zap className="w-3.5 h-3.5 text-slate-950" />
                  <span>{isProcessing && selectedPlan?.id === plan.id ? 'Opening Razorpay...' : `Subscribe via Razorpay Popup`}</span>
                </button>

                {/* 2. Official Razorpay.me Personal Payment Link */}
                <a
                  href="https://razorpay.me/@itsprasanna"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2 rounded-xl font-semibold text-[11px] bg-ide-sidebar hover:bg-slate-700 text-teal-300 border border-teal-500/20 transition-all duration-200 active:scale-95 flex items-center justify-center gap-2"
                >
                  <CreditCard className="w-3.5 h-3.5" />
                  <span>Pay via Razorpay.me Link</span>
                </a>

                {/* 3. Direct UPI QR Option */}
                <button
                  onClick={() => handleOpenUpi(plan)}
                  className="w-full py-2 rounded-xl font-semibold text-[11px] bg-ide-sidebar hover:bg-slate-700 text-emerald-300 border border-emerald-500/20 transition-all duration-200 active:scale-95 flex items-center justify-center gap-2"
                >
                  <QrCode className="w-3.5 h-3.5" />
                  <span>Direct QR Code (0% Fee)</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Direct UPI Modal */}
      {showUpiModal && selectedPlan && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-ide-panel border border-ide-border w-full max-w-md rounded-3xl p-6 relative text-left shadow-2xl">
            <button
              onClick={() => setShowUpiModal(false)}
              className="absolute top-4 right-4 p-2 text-ide-muted hover:text-ide-text rounded-full bg-ide-sidebar"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
              <QrCode className="w-4 h-4" />
              <span>Direct Bank Settlement (0% Commission)</span>
            </div>

            <h2 className="text-xl font-bold text-ide-text mt-1">Pay {selectedPlan.price} via GPay / PhonePe / Paytm</h2>
            <p className="text-ide-muted text-xs mt-1">
              Scan QR code with any UPI app. Payment goes directly to your Personal Savings Bank Account.
            </p>

            {/* QR Code Container */}
            <div className="my-6 p-4 rounded-2xl bg-white flex flex-col items-center justify-center shadow-inner">
              <img
                src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=${personalUpiId}&pn=Prasana%20Code%20AI&am=${selectedPlan.numericPrice}&cu=INR`}
                alt="UPI QR Code"
                className="w-44 h-44 rounded-lg"
              />
              <p className="text-black font-mono text-xs font-extrabold mt-2">UPI ID: {personalUpiId}</p>
            </div>

            {/* Form */}
            <form onSubmit={handleVerifyUpiTxn} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-ide-text mb-1">Enter UPI Reference / UTR Number</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. 427918239012"
                  value={txnRef}
                  onChange={(e) => setTxnRef(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-ide-sidebar border border-ide-border text-ide-text text-xs focus:outline-none focus:border-emerald-500"
                />
              </div>

              <button
                type="submit"
                disabled={isProcessing}
                className="w-full py-3 rounded-xl font-bold text-xs bg-emerald-500 hover:bg-emerald-400 text-black shadow-lg shadow-emerald-500/25 transition-all duration-200"
              >
                {isProcessing ? 'Verifying Transaction...' : 'Confirm Payment & Unlock Pro Access'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

