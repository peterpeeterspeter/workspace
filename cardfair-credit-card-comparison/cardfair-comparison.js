/**
 * Cardfair Credit Card Comparison - JavaScript
 */

(function($) {
    'use strict';

    const CardfairComparison = {
        cards: [],
        filteredCards: [],
        filters: {
            search: '',
            type: 'all',
            issuer: 'all',
            fee: 'all'
        },

        init: function() {
            if (typeof cardfairData === 'undefined') {
                console.error('Cardfair data not loaded');
                return;
            }

            this.cards = cardfairData.cards || [];
            this.filteredCards = [...this.cards];

            this.cacheElements();
            this.bindEvents();
            this.render();
        },

        cacheElements: function() {
            this.$wrapper = $('.cardfair-comparison-wrapper');
            this.$search = this.$wrapper.find('.cardfair-search-input');
            this.$typeFilter = this.$wrapper.find('.cardfair-type-filter');
            this.$issuerFilter = this.$wrapper.find('.cardfair-issuer-filter');
            this.$feeFilter = this.$wrapper.find('.cardfair-fee-filter');
            this.$grid = this.$wrapper.find('.cardfair-cards-grid');
            this.$count = this.$wrapper.find('.cardfair-results-count strong');
        },

        bindEvents: function() {
            const self = this;

            this.$search.on('input', function(e) {
                self.filters.search = $(this).val().toLowerCase();
                self.filterCards();
            });

            this.$typeFilter.on('change', function(e) {
                self.filters.type = $(this).val();
                self.filterCards();
            });

            this.$issuerFilter.on('change', function(e) {
                self.filters.issuer = $(this).val();
                self.filterCards();
            });

            this.$feeFilter.on('change', function(e) {
                self.filters.fee = $(this).val();
                self.filterCards();
            });

            this.$wrapper.on('click', '.cardfair-read-more', function(e) {
                e.preventDefault();
                const $desc = $(this).siblings('.cardfair-card-description');
                $desc.toggleClass('expanded');
                $(this).text($desc.hasClass('expanded') ? 'Show Less' : 'Read More');
            });

            this.$wrapper.on('click', '.cardfair-details-btn', function(e) {
                e.preventDefault();
                const cardName = $(this).data('card-name');
                self.showCardDetails(cardName);
            });
        },

        filterCards: function() {
            const self = this;

            this.filteredCards = this.cards.filter(card => {
                // Search filter
                if (self.filters.search) {
                    const searchStr = self.filters.search;
                    const name = card.name.toLowerCase();
                    const issuer = card.issuer.toLowerCase();
                    const features = (card.additional_features || '').toLowerCase();

                    if (!name.includes(searchStr) &&
                        !issuer.includes(searchStr) &&
                        !features.includes(searchStr)) {
                        return false;
                    }
                }

                // Type filter
                if (self.filters.type !== 'all') {
                    const name = card.name.toLowerCase();

                    switch (self.filters.type) {
                        case 'secured':
                            if (!name.includes('secured')) return false;
                            break;
                        case 'student':
                            if (!name.includes('student')) return false;
                            break;
                        case 'business':
                            if (!name.includes('business')) return false;
                            break;
                        case 'travel':
                            if (!name.includes('travel') &&
                                !name.includes('venture') &&
                                !name.includes('explore')) return false;
                            break;
                        case 'cashback':
                            if (!card.rewards || !card.rewards.toLowerCase().includes('cash')) return false;
                            break;
                    }
                }

                // Issuer filter
                if (self.filters.issuer !== 'all') {
                    if (card.issuer !== self.filters.issuer) return false;
                }

                // Fee filter
                if (self.filters.fee !== 'all') {
                    const fee = card.annual_fee;

                    switch (self.filters.fee) {
                        case 'no-fee':
                            if (!fee.includes('$0') && !fee.includes('None')) return false;
                            break;
                        case 'low-fee':
                            const lowFeeMatch = fee.match(/\$(\d+)/);
                            if (lowFeeMatch && parseInt(lowFeeMatch[1]) > 95) return false;
                            break;
                        case 'premium':
                            const premiumMatch = fee.match(/\$(\d+)/);
                            if (!premiumMatch || parseInt(premiumMatch[1]) < 95) return false;
                            break;
                    }
                }

                return true;
            });

            this.render();
        },

        render: function() {
            this.$count.text(this.filteredCards.length);
            this.$grid.empty();

            if (this.filteredCards.length === 0) {
                this.renderEmptyState();
                return;
            }

            this.filteredCards.forEach((card, index) => {
                const $cardEl = this.createCardElement(card, index);
                this.$grid.append($cardEl);
            });
        },

        createCardElement: function(card, index) {
            const isFeatured = index < 3;
            const cardClass = isFeatured ? 'cardfair-card featured' : 'cardfair-card';

            const $card = $('<div>', {
                class: cardClass,
                itemscope: '',
                itemtype: 'https://schema.org/FinancialProduct'
            });

            // Header
            const $header = $('<div>', {
                class: 'cardfair-card-header'
            });

            const $name = $('<div>', {
                class: 'cardfair-card-name'
            }).append(
                $('<h3>', {
                    text: card.name,
                    itemprop: 'name'
                })
            ).append(
                $('<span>', {
                    class: 'cardfair-card-issuer',
                    text: card.issuer
                })
            );

            $header.append($name);
            $card.append($header);

            // Body
            const $body = $('<div>', {
                class: 'cardfair-card-body'
            });

            // Features tags
            const features = this.extractFeatures(card);
            if (features.length > 0) {
                const $features = $('<div>', {
                    class: 'cardfair-card-features'
                });

                features.slice(0, 4).forEach(feature => {
                    const $tag = $('<span>', {
                        class: 'cardfair-feature-tag' + (feature.highlight ? ' highlight' : ''),
                        text: feature.text
                    });
                    $features.append($tag);
                });

                $body.append($features);
            }

            // Description
            if (card.additional_features) {
                const $desc = $('<div>', {
                    class: 'cardfair-card-description',
                    text: card.additional_features,
                    itemprop: 'description'
                });

                const $readMore = $('<a>', {
                    class: 'cardfair-read-more',
                    text: 'Read More',
                    href: '#'
                });

                $body.append($desc).append($readMore);
            }

            $card.append($body);

            // Stats
            const $stats = $('<div>', {
                class: 'cardfair-card-stats'
            });

            $stats.append(this.createStat('Annual Fee', card.annual_fee, this.getFeeClass(card.annual_fee)));
            $stats.append(this.createStat('Rewards', card.rewards || 'None', 'neutral'));
            $stats.append(this.createStat('Interest Rate', card.interest_rate || 'Varies', 'neutral'));
            $stats.append(this.createStat('Credit Required', card.credit_score_required || 'Varies', 'neutral'));

            $card.append($stats);

            // Footer
            const $footer = $('<div>', {
                class: 'cardfair-card-footer'
            });

            const $applyBtn = $('<a>', {
                class: 'cardfair-apply-btn external',
                href: '#apply-now', // Replace with actual affiliate link
                text: 'Apply Now',
                target: '_blank',
                rel: 'nofollow sponsored'
            });

            const $detailsBtn = $('<button>', {
                class: 'cardfair-details-btn',
                text: 'Details',
                'data-card-name': card.name
            });

            $footer.append($applyBtn).append($detailsBtn);
            $card.append($footer);

            return $card;
        },

        createStat: function(label, value, valueClass) {
            const $stat = $('<div>', {
                class: 'cardfair-stat'
            });

            const $statLabel = $('<div>', {
                class: 'cardfair-stat-label',
                text: label
            });

            const $statValue = $('<div>', {
                class: 'cardfair-stat-value ' + valueClass,
                text: value || 'N/A',
                itemprop: this.getSchemaProp(label)
            });

            return $stat.append($statLabel).append($statValue);
        },

        getFeeClass: function(fee) {
            if (!fee) return 'neutral';

            if (fee.includes('$0') || fee.includes('None')) {
                return 'good';
            } else if (fee.includes('$995') || fee.includes('$695') || fee.includes('$550')) {
                return 'premium';
            } else {
                return 'warning';
            }
        },

        getSchemaProp: function(label) {
            const props = {
                'Annual Fee': 'price',
                'Interest Rate': 'interestRate',
                'Credit Required': 'creditScore'
            };
            return props[label] || '';
        },

        extractFeatures: function(card) {
            const features = [];
            const text = (card.additional_features || '').toLowerCase();
            const name = card.name.toLowerCase();

            // Extract key features
            if (text.includes('0% intro')) {
                features.push({ text: '0% Intro APR', highlight: true });
            }

            if (card.rewards && card.rewards.includes('%')) {
                const rewardsMatch = card.rewards.match(/(\d+%)/);
                if (rewardsMatch) {
                    features.push({ text: rewardsMatch[1] + ' Cash Back', highlight: true });
                }
            }

            if (card.annual_fee && (card.annual_fee.includes('$0') || card.annual_fee.includes('None'))) {
                features.push({ text: 'No Annual Fee', highlight: false });
            }

            if (text.includes('no foreign')) {
                features.push({ text: 'No Foreign Transaction Fee', highlight: false });
            }

            if (name.includes('secured')) {
                features.push({ text: 'Secured Card', highlight: false });
            }

            if (text.includes('credit score') || text.includes('build credit')) {
                features.push({ text: 'Build Credit', highlight: false });
            }

            return features.slice(0, 4);
        },

        renderEmptyState: function() {
            const $empty = $('<div>', {
                class: 'cardfair-empty-state'
            });

            $empty.append(
                $('<div>', { class: 'cardfair-empty-state-icon', text: '🔍' })
            ).append(
                $('<h3>', {
                    class: 'cardfair-empty-state-title',
                    text: 'No cards found'
                })
            ).append(
                $('<p>', {
                    class: 'cardfair-empty-state-text',
                    text: 'Try adjusting your filters to see more results'
                })
            );

            this.$grid.append($empty);
        },

        showCardDetails: function(cardName) {
            const card = this.cards.find(c => c.name === cardName);

            if (!card) return;

            // Create modal with full details
            const modal = $('<div>', {
                class: 'cardfair-modal-overlay'
            });

            const modalContent = $('<div>', {
                class: 'cardfair-modal'
            });

            modalContent.append(
                $('<h2>', { text: card.name })
            ).append(
                $('<p>', { text: card.issuer })
            ).append(
                $('<div>', { html: '<strong>Annual Fee:</strong> ' + card.annual_fee })
            ).append(
                $('<div>', { html: '<strong>Rewards:</strong> ' + (card.rewards || 'None') })
            ).append(
                $('<div>', { html: '<strong>Interest Rate:</strong> ' + (card.interest_rate || 'Varies') })
            ).append(
                $('<div>', { html: '<strong>Features:</strong><br>' + card.additional_features })
            );

            const closeBtn = $('<button>', {
                text: 'Close',
                click: function() {
                    modal.remove();
                }
            });

            modalContent.append(closeBtn);
            modal.append(modalContent);
            $('body').append(modal);
        }
    };

    // Initialize on document ready
    $(document).ready(function() {
        $('.cardfair-comparison-wrapper').each(function() {
            Object.create(CardfairComparison).init();
        });
    });

})(jQuery);
