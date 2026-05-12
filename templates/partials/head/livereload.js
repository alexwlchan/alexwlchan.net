var isPaused = false;

async function startListener() {
  while (true) {
    try {
      const response = await fetch('http://localhost:5555/wait-for-changes');
      
      if (isPaused) {
        console.log("Detected change, but live is disabled")
        break;
      }
      
      if (response.status === 200) {
        console.log("Change detected! Reloading...");
        window.location.reload();
        break;
      }
    } catch (e) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}
startListener();

function pauseLivereload() {
  isPaused = true;
}