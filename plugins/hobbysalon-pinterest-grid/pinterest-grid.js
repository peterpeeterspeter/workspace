/**
 * Hobbysalon Pinterest Grid - JavaScript
 * Masonry layout and interactive features
 */

(function($) {
    'use strict';

    const PinterestGrid = {
        init: function() {
            this.initMasonry();
            this.initSaveButtons();
            this.initLazyLoad();
            this.initAnimations();
        },

        initMasonry: function() {
            const $grid = $('.pinterest-grid');
            
            if ($grid.length === 0) {
                return;
            }

            // Wait for images to load before initializing masonry
            $grid.imagesLoaded(function() {
                // Initialize Masonry
                $grid.masonry({
                    itemSelector: '.pinterest-card',
                    percentPosition: true,
                    horizontalOrder: true,
                    transitionDuration: '0.3s',
                    stagger: 30
                });

                // Relayout on window resize
                let resizeTimer;
                $(window).on('resize', function() {
                    clearTimeout(resizeTimer);
                    resizeTimer = setTimeout(function() {
                        $grid.masonry('layout');
                    }, 250);
                });
            });

            // Also initialize shortcode grids
            $('.pinterest-grid-shortcode').each(function() {
                const $this = $(this);
                $this.imagesLoaded(function() {
                    $this.masonry({
                        itemSelector: '.pinterest-card',
                        percentPosition: true,
                        horizontalOrder: true
                    });
                });
            });
        },

        initSaveButtons: function() {
            $(document).on('click', '.pinterest-card__save', function(e) {
                e.preventDefault();
                e.stopPropagation();

                const $button = $(this);
                const postId = $button.data('post-id');
                
                // Toggle active state
                $button.toggleClass('active');

                // Save to localStorage
                let savedPosts = JSON.parse(localStorage.getItem('hobbysalonSavedPosts') || '[]');
                
                if ($button.hasClass('active')) {
                    if (!savedPosts.includes(postId)) {
                        savedPosts.push(postId);
                    }
                    
                    // Show saved animation
                    $button.addClass('saved');
                    setTimeout(function() {
                        $button.removeClass('saved');
                    }, 1000);
                } else {
                    savedPosts = savedPosts.filter(id => id !== postId);
                }

                localStorage.setItem('hobbysalonSavedPosts', JSON.stringify(savedPosts));

                // Optional: Send to backend
                $.ajax({
                    url: hobbysalonPinterest.ajaxurl,
                    type: 'POST',
                    data: {
                        action: 'hobbysalon_save_post',
                        post_id: postId,
                        nonce: hobbysalonPinterest.nonce
                    },
                    success: function(response) {
                        console.log('Post saved successfully');
                    }
                });
            });

            // Restore saved posts on page load
            this.restoreSavedPosts();
        },

        restoreSavedPosts: function() {
            const savedPosts = JSON.parse(localStorage.getItem('hobbysalonSavedPosts') || '[]');
            
            savedPosts.forEach(function(postId) {
                const $button = $('.pinterest-card__save[data-post-id="' + postId + '"]');
                if ($button.length) {
                    $button.addClass('active');
                }
            });
        },

        initLazyLoad: function() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver(function(entries) {
                    entries.forEach(function(entry) {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            if (img.dataset.src) {
                                img.src = img.dataset.src;
                                img.removeAttribute('data-src');
                                imageObserver.unobserve(img);
                            }
                        }
                    });
                });

                $('.pinterest-card__image img').each(function() {
                    imageObserver.observe(this);
                });
            }
        },

        initAnimations: function() {
            // Animate cards on scroll
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.animationPlayState = 'running';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            $('.pinterest-card').each(function() {
                this.style.animationPlayState = 'paused';
                observer.observe(this);
            });
        }
    };

    // Initialize on document ready
    $(document).ready(function() {
        PinterestGrid.init();
    });

    // Make available globally
    window.HobbysalonPinterestGrid = PinterestGrid;

})(jQuery);

/**
 * ImagesLoaded plugin loader (if not available)
 */
(function() {
    if (typeof jQuery.fn.imagesLoaded === 'undefined') {
        // Simple fallback for images loaded
        jQuery.fn.imagesLoaded = function(callback) {
            const $imgs = this.find('img').add(this.filter('img'));
            const deferred = jQuery.Deferred();
            
            let loaded = 0;
            const total = $imgs.length;

            if (total === 0) {
                deferred.resolve();
                return deferred.promise();
            }

            $imgs.each(function() {
                const img = new Image();
                
                img.onload = img.onerror = function() {
                    loaded++;
                    if (loaded === total) {
                        deferred.resolve();
                    }
                };

                img.src = this.src;
                
                // If already cached
                if (img.complete) {
                    loaded++;
                    if (loaded === total) {
                        deferred.resolve();
                    }
                }
            });

            return deferred.promise(callback);
        };
    }
})();

/**
 * AJAX Handler for saving posts
 */
jQuery(document).ready(function($) {
    // Save post action handler
    $(document).on('click', '.pinterest-card__save', function() {
        const $button = $(this);
        const postId = $button.data('post-id');
        
        // Visual feedback
        if ($button.hasClass('active')) {
            $button.append('<span class="saved-tooltip">Saved!</span>');
            setTimeout(function() {
                $button.find('.saved-tooltip').remove();
            }, 1000);
        }
    });
});
