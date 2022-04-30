import utilities
import matplotlib.pyplot as plt
import numpy


def heatmap():
    with utilities.get_conn() as conn:
        data = utilities.run_query(conn, '''
        select b.x, b.y
        from spaceiq.bookings a

        left join spaceiq.spaces b 
        on a.space = b.idx
        ''')
        heatmap, xedges, yedges = numpy.histogram2d(
            [row['x'] for row in data], 
            [row['y'] for row in data], 
            bins=20
        )
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        plt.imshow(heatmap.T, extent=extent, origin='lower')


def tod():
    with utilities.get_conn() as conn:
        data = utilities.run_query(conn, '''
        select end_dt, start_dt 
        from spaceiq.bookings
        ''')
        hour_histogram = {}
        for hour in range(24):
            hourly_total = sum(
                row['start_dt'].hour <= hour <= row['end_dt'].hour
                for row in data
            )
            if hourly_total != 0:
                hour_histogram[hour] = hourly_total
        plt.bar(
            x=hour_histogram.keys(),
            height=hour_histogram.values(),
        )


def main():
    heatmap()
    plt.show()


if __name__ == '__main__':
    main()