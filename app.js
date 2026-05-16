// MERIT-Net Browser-Side Predictor
// Loads model.json (trained Random Forest) and runs prediction in browser

let MODEL = null;

// Load model
async function loadModel() {
  try {
    const response = await fetch('model.json');
    MODEL = await response.json();
    console.log(`✅ Model loaded: ${MODEL.n_trees} trees`);
  } catch (err) {
    console.error('Failed to load model:', err);
    alert('Error loading prediction model. Please refresh the page.');
  }
}

// Traverse a single decision tree
function predictTree(tree, features) {
  let node = tree;
  while (node.f !== undefined) {
    if (features[node.f] <= node.t) {
      node = node.l;
    } else {
      node = node.r;
    }
  }
  return node.p; // [prob_low, prob_high]
}

// Predict using ensemble of trees
function predictEnsemble(features) {
  if (!MODEL) return null;
  
  const allProbs = MODEL.trees.map(tree => predictTree(tree, features));
  
  // Compute average probabilities
  const avgProbs = [0, 0];
  for (const probs of allProbs) {
    avgProbs[0] += probs[0];
    avgProbs[1] += probs[1];
  }
  avgProbs[0] /= MODEL.n_trees;
  avgProbs[1] /= MODEL.n_trees;
  
  // Predicted class
  const predClass = avgProbs[1] > 0.5 ? 1 : 0;
  
  // ===== Trust Score Computation =====
  // 1. Agreement: how many trees agree on the class
  const treePredictions = allProbs.map(p => p[1] > 0.5 ? 1 : 0);
  const agreementCount = treePredictions.filter(p => p === predClass).length;
  const agreement = agreementCount / MODEL.n_trees;
  
  // 2. Confidence: mean probability of predicted class
  const confidence = avgProbs[predClass];
  
  // 3. Variance stability: 1 - std of predicted class probabilities
  const probsPredClass = allProbs.map(p => p[predClass]);
  const meanProb = probsPredClass.reduce((a, b) => a + b, 0) / probsPredClass.length;
  const variance = probsPredClass.reduce((acc, p) => acc + Math.pow(p - meanProb, 2), 0) / probsPredClass.length;
  const std = Math.sqrt(variance);
  const stability = 1 - std;
  
  // Trust Score formula
  const trustScore = (0.4 * agreement + 0.4 * confidence + 0.2 * stability) * 100;
  
  return {
    predClass: predClass,
    probLow: avgProbs[0],
    probHigh: avgProbs[1],
    trustScore: trustScore,
    agreement: agreement,
    confidence: confidence
  };
}

// Get clinical recommendation based on prediction
function getRecommendation(result) {
  const isHigh = result.predClass === 1;
  const trust = result.trustScore;
  
  if (isHigh && trust >= 95) {
    return "⚠️ <strong>High-risk classification with strong model confidence.</strong> Immediate clinical review and possible specialist referral are recommended.";
  } else if (isHigh && trust >= 85) {
    return "⚠️ <strong>High-risk classification with moderate confidence.</strong> Clinical review is recommended, alongside additional assessments to confirm risk factors.";
  } else if (isHigh && trust < 85) {
    return "⚠️ <strong>High-risk classification with lower confidence.</strong> Detailed clinical evaluation is strongly recommended — model uncertainty suggests additional clinical judgment is needed.";
  } else if (!isHigh && trust >= 95) {
    return "✅ <strong>Low-risk classification with strong model confidence.</strong> Continue with standard antenatal care and routine monitoring.";
  } else if (!isHigh && trust >= 85) {
    return "✅ <strong>Low-risk classification with moderate confidence.</strong> Standard care is appropriate, but continued monitoring is advised.";
  } else {
    return "✅ <strong>Low-risk classification with lower confidence.</strong> Standard care is appropriate, but consider closer monitoring due to model uncertainty.";
  }
}

// Update UI with prediction
function displayResult(result) {
  const resultDiv = document.getElementById('result');
  const riskBadge = document.getElementById('risk-badge');
  const riskLabel = document.getElementById('risk-label');
  const riskProb = document.getElementById('risk-prob');
  const trustScore = document.getElementById('trust-score');
  const trustFill = document.getElementById('trust-fill');
  const trustPct = document.getElementById('trust-pct');
  const recommendation = document.getElementById('recommendation');
  
  // Show result
  resultDiv.classList.remove('hidden');
  
  // Risk badge
  if (result.predClass === 1) {
    riskBadge.className = 'risk-badge high';
    riskLabel.textContent = 'HIGH RISK';
  } else {
    riskBadge.className = 'risk-badge low';
    riskLabel.textContent = 'LOW RISK';
  }
  
  // Metrics
  const probPct = (result.predClass === 1 ? result.probHigh : result.probLow) * 100;
  riskProb.textContent = probPct.toFixed(1) + '%';
  trustScore.textContent = result.trustScore.toFixed(1) + '%';
  
  // Trust bar
  setTimeout(() => {
    trustFill.style.width = result.trustScore + '%';
  }, 100);
  trustPct.textContent = result.trustScore.toFixed(1) + '%';
  
  // Recommendation
  recommendation.innerHTML = getRecommendation(result);
  
  // Scroll into view
  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Get features from form
function getFeatures() {
  return [
    parseFloat(document.getElementById('age').value),
    parseFloat(document.getElementById('sbp').value),
    parseFloat(document.getElementById('dbp').value),
    parseFloat(document.getElementById('bs').value),
    parseFloat(document.getElementById('temp').value),
    parseFloat(document.getElementById('bmi').value),
    parseFloat(document.getElementById('prev').value),
    parseFloat(document.getElementById('pre_diab').value),
    parseFloat(document.getElementById('gest_diab').value),
    parseFloat(document.getElementById('mental').value),
    parseFloat(document.getElementById('hr').value)
  ];
}

// Validate input ranges
function validateInputs() {
  const ranges = {
    age: [10, 70],
    sbp: [60, 250],
    dbp: [30, 160],
    bs: [2, 25],
    temp: [95, 105],
    bmi: [10, 50],
    hr: [40, 150]
  };
  
  for (const [id, [min, max]] of Object.entries(ranges)) {
    const val = parseFloat(document.getElementById(id).value);
    if (isNaN(val) || val < min || val > max) {
      alert(`Please enter a valid value for ${id.toUpperCase()} (${min}-${max})`);
      document.getElementById(id).focus();
      return false;
    }
  }
  return true;
}

// Reset form
function resetForm() {
  document.getElementById('age').value = 30;
  document.getElementById('sbp').value = 120;
  document.getElementById('dbp').value = 80;
  document.getElementById('bs').value = 6.5;
  document.getElementById('temp').value = 98.6;
  document.getElementById('bmi').value = 24.5;
  document.getElementById('hr').value = 76;
  document.getElementById('prev').value = 0;
  document.getElementById('pre_diab').value = 0;
  document.getElementById('gest_diab').value = 0;
  document.getElementById('mental').value = 0;
  document.getElementById('result').classList.add('hidden');
}

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
  await loadModel();
  
  document.getElementById('predict-form').addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (!MODEL) {
      alert('Model is still loading. Please wait a moment.');
      return;
    }
    
    if (!validateInputs()) return;
    
    const features = getFeatures();
    const result = predictEnsemble(features);
    
    if (result) {
      displayResult(result);
    }
  });
  
  document.getElementById('reset-btn').addEventListener('click', resetForm);
});
