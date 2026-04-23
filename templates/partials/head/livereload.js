async function startListener() {
  while (true) {
    try {
      const response = await fetch('http://localhost:5656/wait-for-reload');
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
