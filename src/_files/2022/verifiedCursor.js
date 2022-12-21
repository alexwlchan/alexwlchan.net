/** Based on snowflakeCursor.js, written by Tim Holman and used under the
  * MIT licence.
  * See https://github.com/search?q=cursor-effects&type=repositories
  */
function _svgCursor(svgPath, svgWidth, svgHeight, defaultColor, options) {
  let hasWrapperEl = options && options.element;
  let element = hasWrapperEl || document.body;

  let width = window.innerWidth;
  let height = window.innerHeight;
  let cursor = { x: width / 2, y: width / 2 };
  let particles = [];
  let canvas, context, animationFrame;

  let canvImages = [];

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  );

  // Re-initialise or destroy the cursor when the prefers-reduced-motion setting changes
  prefersReducedMotion.onchange = () => {
    if (prefersReducedMotion.matches) {
      destroy();
    } else {
      init();
    }
  };

  function init() {
    // Don't show the cursor trail if the user has prefers-reduced-motion enabled
    if (prefersReducedMotion.matches) {
      console.log(
        "This browser has prefers reduced motion turned on, so the cursor did not init"
      );
      return false;
    }

    canvas = document.createElement("canvas");
    context = canvas.getContext("2d");

    canvas.style.top = "0px";
    canvas.style.left = "0px";
    canvas.style.pointerEvents = "none";

    if (hasWrapperEl) {
      canvas.style.position = "absolute";
      element.appendChild(canvas);
      canvas.width = element.clientWidth;
      canvas.height = element.clientHeight;
    } else {
      canvas.style.position = "fixed";
      document.body.appendChild(canvas);
      canvas.width = width;
      canvas.height = height;
    }

    let bgCanvas = document.createElement("canvas");
    let bgContext = bgCanvas.getContext("2d");

    let size = options && options.size || 1;

    bgCanvas.width = svgWidth * size;
    bgCanvas.height = svgHeight * size;

    let path = new Path2D(svgPath);
    bgContext.fillStyle = options && options.color ? options.color : defaultColor;
    bgContext.scale(size, size);
    bgContext.fill(path);

    canvImages.push(bgCanvas);

    bindEvents();
    loop();
  }

  // Bind events that are needed
  function bindEvents() {
    element.addEventListener("mousemove", onMouseMove);
    element.addEventListener("touchmove", onTouchMove, { passive: true });
    element.addEventListener("touchstart", onTouchMove, { passive: true });
    window.addEventListener("resize", onWindowResize);
  }

  function onWindowResize(e) {
    width = window.innerWidth;
    height = window.innerHeight;

    if (hasWrapperEl) {
      canvas.width = clientWidth;
      canvas.height = clientHeight;
    } else {
      canvas.width = width;
      canvas.height = height;
    }
  }

  function onTouchMove(e) {
    if (e.touches.length > 0) {
      for (let i = 0; i < e.touches.length; i++) {
        addParticle(
          e.touches[i].clientX,
          e.touches[i].clientY,
          canvImages[Math.floor(Math.random() * canvImages.length)]
        );
      }
    }
  }

  function onMouseMove(e) {
    if (hasWrapperEl) {
      const boundingRect = element.getBoundingClientRect();
      cursor.x = e.clientX - boundingRect.left;
      cursor.y = e.clientY - boundingRect.top;
    } else {
      cursor.x = e.clientX;
      cursor.y = e.clientY;
    }

    addParticle(
      cursor.x,
      cursor.y,
      canvImages[Math.floor(Math.random())]
    );
  }

  function addParticle(x, y, img) {
    if (Math.random() > 1 - (options && options.rate || 1)) {
      particles.push(new Particle(x, y, img));
    }
  }

  function updateParticles() {
    context.clearRect(0, 0, width, height);

    // Update
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(context);
    }

    // Remove dead particles
    for (let i = particles.length - 1; i >= 0; i--) {
      if (particles[i].lifeSpan < 0) {
        particles.splice(i, 1);
      }
    }
  }

  function loop() {
    updateParticles();
    animationFrame = requestAnimationFrame(loop);
  }

  function destroy() {
    canvas.remove();
    cancelAnimationFrame(animationFrame);
    element.removeEventListener("mousemove", onMouseMove);
    element.removeEventListener("touchmove", onTouchMove);
    element.removeEventListener("touchstart", onTouchMove);
    window.addEventListener("resize", onWindowResize);
  };

  /**
   * Particles
   */

  function Particle(x, y, canvasItem) {
    const lifeSpan = Math.floor(Math.random() * 60 + 80);
    this.initialLifeSpan = lifeSpan; //
    this.lifeSpan = lifeSpan; //ms
    this.velocity = {
      x: (Math.random() < 0.5 ? -1 : 1) * (Math.random() / 2),
      y: 1 + Math.random(),
    };
    this.position = { x: x, y: y };
    this.canv = canvasItem;

    this.update = function (context) {
      let size = options && options.size || 1;

      this.position.x += this.velocity.x * size;
      this.position.y += this.velocity.y * size;
      this.lifeSpan--;

      this.velocity.x += ((Math.random() < 0.5 ? -1 : 1) * 2) / 75;
      this.velocity.y -= Math.random() / 300;

      const scale = Math.max(this.lifeSpan / this.initialLifeSpan, 0);

      context.translate(this.position.x, this.position.y);

      context.drawImage(
        this.canv,
        (-this.canv.width / 2) * scale,
        -this.canv.height / 2,
        this.canv.width * scale,
        this.canv.height * scale
      );

      context.translate(-this.position.x, -this.position.y);
    };
  }

  init();

  return {
    destroy: destroy
  }
}

function verifiedCursor(options) {
  return _svgCursor(
    'M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91c-1.31.67-2.2 1.91-2.2 3.34s.89 2.67 2.2 3.34c-.46 1.39-.21 2.9.8 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.45 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34zm-11.71 4.2L6.8 12.46l1.41-1.42 2.26 2.26 4.8-5.23 1.47 1.36-6.2 6.77z',
    24, 24, '#55acee',
    options
  );
}

function unverifiedCursor(options) {
  return _svgCursor(
    'M8.603 3.799A4.49 4.49 0 0112 2.25c1.357 0 2.573.6 3.397 1.549a4.49 4.49 0 013.498 1.307 4.491 4.491 0 011.307 3.497A4.49 4.49 0 0121.75 12a4.49 4.49 0 01-1.549 3.397 4.491 4.491 0 01-1.307 3.497 4.491 4.491 0 01-3.497 1.307A4.49 4.49 0 0112 21.75a4.49 4.49 0 01-3.397-1.549 4.49 4.49 0 01-3.498-1.306 4.491 4.491 0 01-1.307-3.498A4.49 4.49 0 012.25 12c0-1.357.6-2.573 1.549-3.397a4.49 4.49 0 011.307-3.497 4.49 4.49 0 013.497-1.307zM14.47 11.78a 0.75,0.75 0 0 0 1.06,-1.06l -2.25,-2.25a 0.75,0.75 0 0 0 -1.14,0.094l -3.75,5.25a 0.75,0.75 0 1 0 1.22,0.872l 3.236,-4.53z',
    24, 24, '#83254f',
    options
  );
}
