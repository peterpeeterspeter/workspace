import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
export function WireframeCube() {
  const containerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;
    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 3;
    // Renderer
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;
    // Create wireframe cube with neon edges
    const geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
    const edges = new THREE.EdgesGeometry(geometry);
    // Main cube - green
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x00ff9f,
      linewidth: 2
    });
    const cube = new THREE.LineSegments(edges, lineMaterial);
    scene.add(cube);
    // Inner cube - pink
    const innerGeometry = new THREE.BoxGeometry(1, 1, 1);
    const innerEdges = new THREE.EdgesGeometry(innerGeometry);
    const innerMaterial = new THREE.LineBasicMaterial({
      color: 0xff00ff,
      linewidth: 2
    });
    const innerCube = new THREE.LineSegments(innerEdges, innerMaterial);
    scene.add(innerCube);
    // Outer cube - cyan
    const outerGeometry = new THREE.BoxGeometry(2, 2, 2);
    const outerEdges = new THREE.EdgesGeometry(outerGeometry);
    const outerMaterial = new THREE.LineBasicMaterial({
      color: 0x00d9ff,
      linewidth: 1,
      transparent: true,
      opacity: 0.5
    });
    const outerCube = new THREE.LineSegments(outerEdges, outerMaterial);
    scene.add(outerCube);
    // Floating particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particleCount = 100;
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 5;
      positions[i + 1] = (Math.random() - 0.5) * 5;
      positions[i + 2] = (Math.random() - 0.5) * 5;
    }
    particlesGeometry.setAttribute(
      'position',
      new THREE.BufferAttribute(positions, 3)
    );
    const particlesMaterial = new THREE.PointsMaterial({
      color: 0x00ff9f,
      size: 0.02,
      transparent: true,
      opacity: 0.8
    });
    const particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);
    // Animation
    let animationId: number;
    const animate = () => {
      animationId = requestAnimationFrame(animate);
      cube.rotation.x += 0.003;
      cube.rotation.y += 0.005;
      innerCube.rotation.x -= 0.004;
      innerCube.rotation.y -= 0.006;
      outerCube.rotation.x += 0.001;
      outerCube.rotation.y += 0.002;
      particles.rotation.y += 0.001;
      renderer.render(scene, camera);
    };
    animate();
    // Handle resize
    const handleResize = () => {
      if (!containerRef.current) return;
      const newWidth = containerRef.current.clientWidth;
      const newHeight = containerRef.current.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };
    window.addEventListener('resize', handleResize);
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, []);
  return (
    <div
      ref={containerRef}
      className="w-full h-full min-h-[400px]"
      aria-hidden="true" />);


}