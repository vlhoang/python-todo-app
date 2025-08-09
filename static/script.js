// Helper: format date like "January 18, 9:00 PM"
function formatDateTime(d) {
  const months = [
    'January','February','March','April','May','June','July','August','September','October','November','December'
  ];
  const month = months[d.getMonth()];
  const day = d.getDate();
  let hours = d.getHours();
  const minutes = d.getMinutes();
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 -> 12
  const mins = minutes < 10 ? '0' + minutes : minutes;
  return `${month} ${day}, ${hours}:${mins} ${ampm}`;
}

function updateDateTime() {
  const now = new Date();
  document.getElementById('datetime').textContent = formatDateTime(now);
}

// Fetch random travel photo from Unsplash Source (no API key required)
function setBackgroundFromUnsplash() {
  document.body.style.backgroundImage = `url('/static/images/house_winter_snow_134709_3840x2160.jpg')`;
  // Add a cache-buster to get a fresh image on each load if desired
}

// Fetch a random quote from Quotable
async function fetchQuote() {
  try {
    const response = await fetch('/quote'); // Fetch from your Python backend
    const data = await response.json();
        // Assuming your server returns something like:
        // { "quote": "Life is short", "author": "Someone" }
    const quoteEl = document.getElementById('quote');
    quoteEl.textContent = `"${data.quote}" — ${data.author}`;
  } catch (err) {
    document.getElementById('quote').textContent = 'Could not load quote.';
    console.error(err);
  }
}

// Init on load
window.addEventListener('load', function() {
  setBackgroundFromUnsplash();
  updateDateTime();
  fetchQuote();
  setInterval(updateDateTime, 1000);

  // Re-fetch background on visibility/gain focus to get new image occasionally (optional)
  window.addEventListener('focus', () => {
    // small chance to refresh; comment out if not desired
    // setBackgroundFromUnsplash();
  });
});