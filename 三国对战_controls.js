
// Update visibility of mobile controls based on game state
function updateControlsVisibility() {
    if (!isMobile) return;
    
    const controls = document.getElementById('controls');
    const mobileUtils = document.getElementById('mobileUtils');
    
    // Only show controls during active battle
    const showControls = (gameState === 'battle');
    
    if (controls) {
        controls.style.display = showControls ? 'block' : 'none';
    }
    
    if (mobileUtils) {
        mobileUtils.style.display = showControls ? 'flex' : 'none';
    }
}
