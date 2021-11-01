// # seconds to animation end
var animTime = 480000; // ~8 minutes for all tweets with pics, reduce for text-only tweets

$(function() {
  loadTwitterWidget();
});

function loadTwitterWidget() {
  var timelineData = [
    {
      sourceType: "profile",
      screenName: "Reuters"
    },
    $("#twit")[0],
    {
      chrome: "noheader nofooter noscrollbar noborders transparent",
      height: 400,
      width: 600
    }
  ];

  // injected iframe element(s) after twitter API finds widgets
  var iframe;

  // element(s) we want to scroll
  var viewport;

  // initial scroll distance
  var initialDistance;

  // restart scroll on new tweet since twttr does not have a new tweet event
  var newTweetObserver = new MutationObserver(scroll);

  // hide elements we do not want to see
  function getElemsToHide() {
    return [
      $(".timeline-InformationCircle", iframe),
      $(".timeline-LoadMore", iframe),
      $(".timeline-NewTweetsNotification", iframe)
    ];
  }

  function hideElements(elems) {
    for (var i = 0; i < elems.length; i++) {
      elems[i].hide();
    }
  }

  function scroll() {
    // reset to top
    viewport.stop().scrollTop(0);

    hideElements(getElemsToHide());

    // calculate new distance assuming height is varied
    var distance =
      viewport.prop("scrollHeight") -
      viewport.prop("scrollTop") -
      viewport.height();

    // calculate duration based on initial speed to ensure uniform scroll speed
    var duration = animTime * (distance / initialDistance);

    // if there is something to scroll
    if (viewport.prop("scrollHeight") > viewport.height()) {
      viewport.animate(
        {
          scrollTop: distance
        },
        {
          easing: "linear",
          duration: duration,
          done: scroll
        }
      );
    }
  }

  twttr.ready(function(twttr) {
    // create twitter timeline
    // IE11 can't handle Rest parameters. If you want to support IE11, use the following line instead:
    // twttr.widgets.createTimeline.apply(this, timelineData);
    twttr.widgets.createTimeline(...timelineData);

    // twitter widgets are rendered
    twttr.events.bind("rendered", function(event) {
      // hide "more tweets" links/info buttons that may be injected
      hideElements(getElemsToHide());

      // injected iframe element(s) after twitter API finds widgets
      iframe = $(event.target).contents();

      // element(s) we want to scroll
      viewport = $(".timeline-Viewport", iframe);

      // initial scroll distance
      initialDistance = viewport.prop("scrollHeight") - viewport.height();

      // pass in the target node, as well as the observer options
      newTweetObserver.observe($(".timeline-TweetList", iframe)[0], {
        childList: true
      });

      scroll();
    });
  });
}