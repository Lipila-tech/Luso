/**
* Project Name: Lipila Patron
* Updated: 29 June 2024 Lipila Patron v1
* Author: Peter Zyambo
* License:
*/


/**
 * Listens to the submmision of a depositi form and gets the forms ids.
 */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('form[id^="approve-form-"], form[id^="reject-form-"]').forEach(form => {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const formId = this.id.split('-').pop();  // Get the form identifier
      const action = this.id.split('-')[0];
      const amount = document.getElementById(`id_amount-${formId}`).value;
      const accountNumber = document.getElementById(`id_account_number-${formId}`).value;

      if (action == 'approve') {
        if (confirm(`Confirm disbursement of K${amount} to ${accountNumber}`) == true) {
          initiateDeposit(formId, action);
        }
      } else {
        if (confirm(`Reject withdraw of K${amount} from ${accountNumber}`) == true) {
          initiateDeposit(formId, action);
        }
      }
    });
  });
});

/**
 * This function queries the api to disburse funds.
 * @param {The id of the form to be submitted} formId
 * @param {The action to be taken} action
 */

async function initiateDeposit(formId, action) {
  document.getElementById('loader').style.display = 'block';
  const amount = document.getElementById(`id_amount-${formId}`).value;
  const description = document.getElementById(`id_reason-${formId}`).value;
  const accountNumber = document.getElementById(`id_account_number-${formId}`).value;
  const paymentMethod = document.getElementById(`id_payment_method-${formId}`).value;
  const requestId = document.getElementById(`id_request-${formId}`).value;

  const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  try {
    const response = await fetch('http://localhost:8000/approve_withdrawals/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        action: action, request_id: requestId, amount: amount,
        payee_account_number: accountNumber,
        description: description, payment_method: paymentMethod
      })
    });

    if (!response.ok) {
      document.getElementById('loader').style.display = 'none';
      throw new Error(`Error initiating payment: ${response.statusText}`);
    }

    const data = await response.json();

    if (data.message === 'Payment initiated successfully') {
      document.getElementById('loader').style.display = 'none';
      const referenceId = data.reference_id;
      redirectToApproveRequest();
    } else {
      document.getElementById('loader').style.display = 'none';
      redirectToApproveRequest();
    }
  } catch (error) {
    document.getElementById('loader').style.display = 'none';
    redirectToApproveRequest();
  } finally {
    // Optional cleanup actions
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const paymentForm = document.getElementById('contribute-form');

  if (paymentForm) {
    paymentForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const tierId = document.getElementById('id_request').value;
      const requestType = document.getElementById('requestType').value;

      if (confirm('You will be asked to confirm payment on your mobile.') == true) {
        initiatePayment(tierId, 'contribute');
      }
    });
  } else {
    console.error('The payment form with id "contribute-form" was not found.');
  }
});

/**
 * Listens to submmission of the payment form and
 */
document.addEventListener("DOMContentLoaded", () => {
  const paymentForm = document.getElementById('payment-form');

  if (paymentForm) {
    paymentForm.addEventListener('submit', function (event) {
      event.preventDefault();
      const tierId = document.getElementById('id_request').value;
      const requestType = document.getElementById('requestType').value;

      if (confirm('You will be asked to confirm payment on your mobile.') == true) {
          initiatePayment(tierId, 'pay');
      }
    });
  } else {
    console.error('The payment form with id "payment-form" was not found.');
  }
});


/**
 * This function queries the collections endpoint to initiae payment.
 * @param {*} id_request 
 * @param {*} requestType 
 */

async function initiatePayment(id_request, requestType) {
  document.getElementById('loader').style.display = 'block';
  const paymentMethod = document.getElementById('id_payment_method').value;  // Access value using ID
  const amount = document.getElementById('id_amount').value;
  const phoneNumber = document.getElementById('id_payer_account_number').value;
  const description = document.getElementById('id_description').value;


  const csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;  // Get CSRF token from the form

  try {
    const response = await fetch(`http://localhost:8000/patron/payments/${requestType}/${id_request}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify(
        { amount: amount, payment_method: paymentMethod, payer_account_number: phoneNumber, description: description })  // Send payment amount in JSON format
    });

    if (!response.ok) {
      document.getElementById('loader').style.display = 'none';
      throw new Error(`Error initiating payment: ${response.statusText}`);
    }

    const data = await response.json();  // Parse JSON response

    if (data.message === 'Payment initiated successfully') {
      document.getElementById('loader').style.display = 'none';
      // Handle successful payment initiation
      const referenceId = data.reference_id;
      redirectToPaymentHistory(requestType);
    } else {
      document.getElementById('loader').style.display = 'none';
      // alert('Error: ' + data.error);  // Handle potential error message from the view
      redirectToPayment(requestType, id_request)
    }
  } catch (error) {
    document.getElementById('loader').style.display = 'none';
    redirectToPayment(requestType, id_request)
  } finally {
    // Perform any cleanup actions after the request completes (optional)
  }
}

/**
 * 
 * @param {*} endpoint 
 */
function redirectToPaymentHistory(endpoint) {
  window.location.href = `http://localhost:8000/patron/history/${endpoint}`;
}

/**
 * 
 * @param {*} endpoint 
 * @param {*} id_request 
 */
function redirectToPayment(endpoint, id_request) {
  window.location.href = `http://localhost:8000/patron/payments/${endpoint}/${id_request}`
}

/**
 * Redirects user to the processed withdrawals
 */
function redirectToProcessed() {
  window.location.href = 'http://localhost:8000/processed_withdrawals/'
}

/**
 * Redirects a user to Approve Withdrawals
 */
function redirectToApproveRequest() {
  window.location.href = 'http://localhost:8000/approve_withdrawals/'
}


const closeButtons = document.querySelectorAll('.close-btn');

closeButtons.forEach(closeButton => {
  closeButton.addEventListener('click', function () {
    const messageDiv = this.parentElement;  // Get the parent message div
    messageDiv.style.display = 'none';  // Hide the message div
  });
});


const copyButtons = document.querySelectorAll('.copy-btn');

copyButtons.forEach(button => {
  button.addEventListener('click', () => {
    const url = button.dataset.clipboardText;
    navigator.clipboard.writeText(url)
      .then(() => {
        button.textContent = 'Copied!'; // Success message
      })
      .catch(err => {
        console.error('Failed to copy:', err); // Handle errors in development
        button.textContent = 'Copy failed'; // Error message
      });
    setTimeout(() => {
      button.textContent = 'Copy'; // Reset button text after a short delay
    }, 2000); // Adjust delay as needed
  });
});


document.addEventListener('DOMContentLoaded', () => {
  "use strict";

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Scroll up sticky header to headers with .scroll-up-sticky class
   */
  let lastScrollTop = 0;
  window.addEventListener('scroll', function () {
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky')) return;

    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = `-${header.offsetHeight + 50}px`;
    } else if (scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = "0";
    } else {
      selectHeader.style.removeProperty('top');
      selectHeader.style.removeProperty('position');
    }
    lastScrollTop = scrollTop;
  });

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .has-dropdown i').forEach(navmenu => {
    navmenu.addEventListener('click', function (e) {
      if (document.querySelector('.mobile-nav-active')) {
        e.preventDefault();
        this.parentNode.classList.toggle('active');
        this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
        e.stopImmediatePropagation();
      }
    });
  });

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function (e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Initiate Pure Counter
   */
  // new PureCounter();

  /**
   * Init isotope layout and filters
   */
  function initIsotopeLayout() {
    document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
      let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
      let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
      let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

      let initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });

      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
        filters.addEventListener('click', function () {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({
            filter: this.getAttribute('data-filter')
          });
          if (typeof aosInit === 'function') {
            aosInit();
          }
        }, false);
      });

    });
  }
  window.addEventListener('load', initIsotopeLayout);

  /**
   * Frequently Asked Questions Toggle
   */
  document.querySelectorAll('.faq-item h3, .faq-item .faq-toggle').forEach((faqItem) => {
    faqItem.addEventListener('click', () => {
      faqItem.parentNode.classList.toggle('faq-active');
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll('.swiper').forEach(function (swiper) {
      let config = JSON.parse(swiper.querySelector('.swiper-config').innerHTML.trim());
      new Swiper(swiper, config);
    });
  }
  window.addEventListener('load', initSwiper);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

});

// Nice Admin
(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function (e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function (e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
            color: []
          },
          {
            background: []
          }
          ],
          [{
            script: "super"
          },
          {
            script: "sub"
          }
          ],
          [{
            list: "ordered"
          },
          {
            list: "bullet"
          },
          {
            indent: "-1"
          },
          {
            indent: "+1"
          }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */
  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  /**
   * Handle withdraw button
   */
  document.getElementById('withdraw-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form from submitting immediately
    const accountNumber = document.getElementById('account-number').value;
    const accountName = document.getElementById('account-name').value;
    const amount = document.getElementById('amount').value;

    const confirmation = confirm(`Are you sure you want to withdraw ZMW ${amount} using account ${accountName} (Account Number: ${accountNumber})?`);
    if (confirmation) {
      this.submit(); // Submit the form if the user confirms
    }
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [5, 10, 15, ["All", -1]],
      columns: [{
        select: 2,
        sortSequence: ["desc", "asc"]
      },
      {
        select: 3,
        sortSequence: ["desc"]
      },
      {
        select: 4,
        cellClass: "green",
        headerClass: "red"
      }
      ]
    });
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function () {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

})();