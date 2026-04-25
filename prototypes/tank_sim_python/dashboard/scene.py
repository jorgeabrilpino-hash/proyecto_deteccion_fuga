from __future__ import annotations

import json


def build_tank_scene_html(state: dict) -> str:
    payload = json.dumps(state)
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <style>
    html, body {{ margin: 0; padding: 0; background: #07111f; color: #d9e7ff; font-family: Arial, sans-serif; }}
    #wrap {{ position: relative; width: 100%; height: 700px; overflow: hidden; border-radius: 18px; background: radial-gradient(circle at top, #11233f 0%, #07111f 70%); }}
    #overlay {{ position: absolute; top: 16px; left: 16px; z-index: 10; background: rgba(8, 19, 36, 0.78); padding: 14px 16px; border-radius: 14px; backdrop-filter: blur(6px); min-width: 250px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }}
    #overlay h3 {{ margin: 0 0 10px 0; font-size: 18px; }}
    #overlay .row {{ margin: 6px 0; font-size: 13px; color: #c7d7f2; }}
    #sensorInfo {{ position: absolute; right: 16px; top: 16px; z-index: 10; background: rgba(8, 19, 36, 0.78); padding: 12px 14px; border-radius: 14px; max-width: 280px; min-height: 72px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }}
    #legend {{ position: absolute; left: 16px; bottom: 16px; z-index: 10; background: rgba(8, 19, 36, 0.72); padding: 12px 14px; border-radius: 14px; font-size: 12px; color: #c7d7f2; }}
    canvas {{ display: block; }}
    .pill {{ display: inline-block; padding: 4px 8px; border-radius: 999px; font-size: 11px; margin-top: 8px; background: #133154; color: #d8ebff; }}
  </style>
</head>
<body>
  <div id=\"wrap\">
    <div id=\"overlay\">
      <h3>Simulación 3D del tanque</h3>
      <div class=\"row\"><strong>Estado:</strong> <span id=\"statusText\"></span></div>
      <div class=\"row\"><strong>Nivel:</strong> <span id=\"levelText\"></span></div>
      <div class=\"row\"><strong>Presión:</strong> <span id=\"pressureText\"></span></div>
      <div class=\"row\"><strong>Flujo izquierdo:</strong> <span id=\"leftFlowText\"></span></div>
      <div class=\"row\"><strong>Flujo derecho:</strong> <span id=\"rightFlowText\"></span></div>
      <div class=\"pill\">Haz clic sobre cámaras o sensores</div>
    </div>
    <div id=\"sensorInfo\">Selecciona un sensor o cámara para ver detalle.</div>
    <div id=\"legend\">
      Verde, estado normal<br/>
      Amarillo, advertencia<br/>
      Rojo, anomalía o fuga
    </div>
  </div>

  <script type=\"module\">
    import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
    import {{ OrbitControls }} from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

    const state = {payload};
    const wrap = document.getElementById('wrap');
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x07111f, 10, 35);

    const camera = new THREE.PerspectiveCamera(48, wrap.clientWidth / wrap.clientHeight, 0.1, 100);
    camera.position.set(7, 5, 8);

    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(wrap.clientWidth, wrap.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    wrap.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.target.set(0, 2, 0);

    const ambient = new THREE.AmbientLight(0xffffff, 1.2);
    scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xaed1ff, 2.2);
    dirLight.position.set(10, 12, 8);
    scene.add(dirLight);
    const backLight = new THREE.PointLight(0x5ca9ff, 30, 40);
    backLight.position.set(-6, 5, -6);
    scene.add(backLight);

    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(8, 64),
      new THREE.MeshStandardMaterial({{ color: 0x13243b, roughness: 0.92, metalness: 0.08 }})
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    const tankGroup = new THREE.Group();
    scene.add(tankGroup);

    const shellMaterial = new THREE.MeshPhysicalMaterial({{
      color: 0x9ba8ba,
      metalness: 0.55,
      roughness: 0.24,
      transparent: true,
      opacity: 0.3,
      side: THREE.DoubleSide,
      transmission: 0.35,
    }});
    const tankShell = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.9, 4.6, 64, 1, true), shellMaterial);
    tankShell.position.y = 2.3;
    tankGroup.add(tankShell);

    const topRing = new THREE.Mesh(new THREE.TorusGeometry(1.92, 0.05, 16, 64), new THREE.MeshStandardMaterial({{ color: 0x8ea6c1, metalness: 0.6, roughness: 0.25 }}));
    topRing.position.y = 4.6;
    topRing.rotation.x = Math.PI / 2;
    tankGroup.add(topRing);

    const bottomRing = topRing.clone();
    bottomRing.position.y = 0;
    tankGroup.add(bottomRing);

    const level = Math.max(0.12, Math.min(0.95, state.level_pct / 100));
    const liquidHeight = 4.2 * level;
    const liquid = new THREE.Mesh(
      new THREE.CylinderGeometry(1.78, 1.78, liquidHeight, 48),
      new THREE.MeshPhysicalMaterial({{ color: state.leak_detected ? 0xff7b6b : 0x32b5ff, transparent: true, opacity: 0.72, transmission: 0.1, roughness: 0.18 }})
    );
    liquid.position.y = liquidHeight / 2 + 0.18;
    tankGroup.add(liquid);

    const liquidTop = new THREE.Mesh(
      new THREE.CircleGeometry(1.78, 48),
      new THREE.MeshBasicMaterial({{ color: 0x8de3ff, transparent: true, opacity: 0.35 }})
    );
    liquidTop.rotation.x = -Math.PI / 2;
    liquidTop.position.y = liquid.position.y + liquidHeight / 2 - 0.01;
    tankGroup.add(liquidTop);

    function buildPipe(xDir, flowValue) {{
      const pipeGroup = new THREE.Group();
      const pipe = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.14, 2.3, 24),
        new THREE.MeshStandardMaterial({{ color: 0xb4bfd0, metalness: 0.5, roughness: 0.32 }})
      );
      pipe.rotation.z = Math.PI / 2;
      pipe.position.set(2.4 * xDir, 1.8, 0);
      pipeGroup.add(pipe);

      const valve = new THREE.Mesh(
        new THREE.TorusGeometry(0.24, 0.06, 12, 24),
        new THREE.MeshStandardMaterial({{ color: flowValue > 1 ? 0x68f2a3 : 0x9aaac2, metalness: 0.45, roughness: 0.3 }})
      );
      valve.position.set(3.35 * xDir, 1.8, 0);
      valve.rotation.y = Math.PI / 2;
      pipeGroup.add(valve);

      if (flowValue > 1) {{
        const stream = new THREE.Mesh(
          new THREE.CylinderGeometry(0.05, 0.05, 1.2, 12),
          new THREE.MeshBasicMaterial({{ color: 0x5ed7ff, transparent: true, opacity: 0.85 }})
        );
        stream.position.set(4.2 * xDir, 1.2, 0);
        pipeGroup.add(stream);
      }}
      return pipeGroup;
    }}

    tankGroup.add(buildPipe(-1, state.flow_left_lpm));
    tankGroup.add(buildPipe(1, state.flow_right_lpm));

    const clickable = [];
    function addSensor(name, color, position, details) {{
      const body = new THREE.Mesh(
        new THREE.BoxGeometry(0.42, 0.22, 0.42),
        new THREE.MeshStandardMaterial({{ color }})
      );
      body.position.copy(position);
      body.userData = {{ name, details }};
      clickable.push(body);
      scene.add(body);
      return body;
    }}

    const pressureColor = state.pressure_kpa < 35 ? 0xff5c5c : 0x66ffb3;
    addSensor('Sensor de presión', pressureColor, new THREE.Vector3(0, 4.85, 0), `Presión actual: ${{state.pressure_kpa}} kPa`);

    const leftCam = addSensor('Cámara lateral izquierda', 0x6aa8ff, new THREE.Vector3(-4.4, 3.1, 2.6), 'Observa lado izquierdo del tanque y tubería.');
    const rightCam = addSensor('Cámara lateral derecha', 0x6aa8ff, new THREE.Vector3(4.4, 3.1, 2.6), 'Observa lado derecho del tanque y tubería.');

    const leftCamStand = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.3, 12), new THREE.MeshStandardMaterial({{ color: 0x8797b2 }}));
    leftCamStand.position.set(-4.4, 1.95, 2.6); scene.add(leftCamStand);
    const rightCamStand = leftCamStand.clone(); rightCamStand.position.set(4.4, 1.95, 2.6); scene.add(rightCamStand);

    const leakPad = new THREE.Mesh(
      new THREE.CylinderGeometry(1.4, 1.4, 0.03, 32),
      new THREE.MeshBasicMaterial({{ color: state.leak_detected ? 0xff4d4d : 0x2d4a6d, transparent: true, opacity: state.leak_detected ? 0.95 : 0.35 }})
    );
    leakPad.position.y = 0.03;
    scene.add(leakPad);
    leakPad.userData = {{ name: 'Base de fuga', details: state.leak_detected ? 'Se detecta fuga simulada en la base del tanque.' : 'No se detecta fuga visible en la base.' }};
    clickable.push(leakPad);

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const sensorInfo = document.getElementById('sensorInfo');

    renderer.domElement.addEventListener('click', (event) => {{
      const rect = renderer.domElement.getBoundingClientRect();
      pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(pointer, camera);
      const hits = raycaster.intersectObjects(clickable, false);
      if (hits.length) {{
        const obj = hits[0].object;
        sensorInfo.innerHTML = `<strong>${{obj.userData.name}}</strong><br/><span style="font-size:13px;color:#c7d7f2;">${{obj.userData.details}}</span>`;
      }}
    }});

    function setText(id, value) {{ document.getElementById(id).textContent = value; }}
    setText('statusText', state.status_label);
    setText('levelText', `${state.level_pct}%`);
    setText('pressureText', `${state.pressure_kpa} kPa`);
    setText('leftFlowText', `${state.flow_left_lpm} L/min`);
    setText('rightFlowText', `${state.flow_right_lpm} L/min`);

    const statusColor = state.leak_detected ? 0xff6b6b : (state.pressure_kpa < 35 ? 0xffd166 : 0x66f2a3);
    const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.18, 24, 24), new THREE.MeshBasicMaterial({{ color: statusColor }}));
    beacon.position.set(0, 5.2, 0);
    scene.add(beacon);

    window.addEventListener('resize', () => {{
      camera.aspect = wrap.clientWidth / wrap.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(wrap.clientWidth, wrap.clientHeight);
    }});

    let t = 0;
    function animate() {{
      requestAnimationFrame(animate);
      t += 0.02;
      liquidTop.position.y += Math.sin(t) * 0.002;
      beacon.scale.setScalar(1 + Math.sin(t * 2.2) * 0.08);
      leftCam.lookAt(0, 2.5, 0);
      rightCam.lookAt(0, 2.5, 0);
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();
  </script>
</body>
</html>
"""
